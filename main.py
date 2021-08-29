# imports
import time
import logging

# services
from services.email_service import EmailService
from services.reddit_service import RedditService
from services.alert_service import AlertService
from services.uptime_service import UptimeService
from services.post_analyzer_service import PostAnalyzerService
from services.page_search_service import PageSearchService
from services.user_service import UserService

# objects
from objects.app_info import AppInfo

# globals
SLEEP_INTERVAL_M = 10

# logging config
# TODO adding logging service
LOGGING_LEVEL = logging.INFO
FORMAT = '[%(asctime)s] %(levelname)-7s %(message)s'
logging.basicConfig(level=LOGGING_LEVEL, format=FORMAT, filename='log.log')


def main():
    # populate globals
    app_info = AppInfo()

    # initialize services
    uptime_service = UptimeService(time.time())  # populates the uptime service with the current time for start time
    email_service = EmailService(app_info.sender_email, app_info.sender_email_password, app_info.user_agent, uptime_service)
    reddit_service = RedditService(app_info.client_id, app_info.client_secret, app_info.user_agent)
    alert_service = AlertService()
    post_analyzer_service = PostAnalyzerService(reddit_service, alert_service, email_service)
    page_search_service = PageSearchService(alert_service, email_service)
    user_service = UserService()

    # send startup notification
    email_service.send_startup_email(app_info.maintenance_email)

    # do forever
    while True:
        try:
            for user in user_service.get_users():

                # search reddit if we want to
                if user.keywords and user.subreddits:
                    post_analyzer_service.analyze_posts(user)

                # search urls if we want to
                if user.urls:
                    page_search_service.analyze_pages(user)

            # take a nap
            logging.info(f"{uptime_service.get().ljust(18)} : Sleeping for {SLEEP_INTERVAL_M} minutes...")
            time.sleep(SLEEP_INTERVAL_M * 60)

        # uh oh
        except Exception as e:
            if e.response is not None and e.response.status_code == 401:
                # check if it's a 401, which is probably just a config issue
                logging.error(f'Received a 401 response code from reddit')
                email_service.send_shutdown_email(e, app_info.maintenance_email)
                time.sleep(10)
                quit()
            elif e.response is not None and e.response.status_code == 404:
                # this will probably happen for any 404s while page searching
                logging.error(f'Received a 404 response from a page searching')
                # just continue for now until I decide what to do
            elif e.response is not None and e.response.status_code == 503:
                # check if it's a 503, which means reddit is down
                logging.error(f'Received a 503 response code from reddit')
                # we just want to continue in this case, because reddit will be up again soon... right?
            else:
                # catch all
                logging.error(f'Unknown exception caught in main loop:')
                logging.error(f'{e}')
                email_service.send_shutdown_email(e, app_info.maintenance_email)
                time.sleep(10)
                quit()


if __name__ == "__main__":
    main()

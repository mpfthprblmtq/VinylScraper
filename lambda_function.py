# imports
import traceback

# _services
from _services.email_service import EmailService
from _services.reddit_service import RedditService
from _services.alert_service import AlertService
from _services.page_search_service import PageSearchService
from _services.twitter_service import TwitterService
from _services.user_service import UserService
from _services.logging_service import Logger

# _objects
from _objects.app_info import AppInfo


def lambda_handler(event, context):
    # populate globals
    app_info = AppInfo()

    # initialize the logger
    logger = Logger()

    # initialize _services
    email_service = EmailService(
        app_info.sender_email,
        app_info.sender_email_password,
        app_info.user_agent,
        logger)
    alert_service = AlertService(logger)
    reddit_service = RedditService(
        app_info.reddit_client_id,
        app_info.reddit_client_secret,
        app_info.user_agent,
        alert_service,
        email_service,
        logger)
    page_search_service = PageSearchService(alert_service, email_service, logger)
    twitter_service = TwitterService(app_info.twitter_bearer_token, email_service, alert_service, logger)
    user_service = UserService()

    # errors to return
    errors = []

    # do the thing
    try:
        for user in user_service.get_users():

            # search reddit if we want to
            if user.reddit_keywords and user.subreddits:
                reddit_service.analyze_posts(user)

            # search urls if we want to
            if user.urls:
                page_search_service.analyze_pages(user)

            # search twitter if we want to
            if user.twitter_profiles:
                twitter_service.search_tweets(user)

    # uh oh
    except Exception as e:
        if hasattr(e, 'code') and e.code == 103:
            # fail silently
            logger.error('Main', f'Received a 103 response from a page searching: {e.filename}')
            errors.append(f'Received a 103 response from a page searching: {e.filename}')
        elif hasattr(e, 'code') and e.code == 401:
            # check if it's a 401, which is probably just a config issue
            logger.error('Main', f'Received a 401 response code from reddit')
            errors.append(f'Received a 401 response code from reddit')
        elif hasattr(e, 'code') and e.code == 404:
            # this will probably happen for any 404s while page searching
            logger.error('Main', f'Received a 404 response from a page searching: {e.filename}')
            errors.append(f'Received a 404 response from a page searching: {e.filename}')
        elif hasattr(e, 'code') and e.code == 503:
            # check if it's a 503, which means reddit is down
            logger.error('Main', f'Received a 503 response code: {e.filename}')
            errors.append(f'Received a 503 response code: {e.filename}')
        else:
            # catch all
            logger.error_with_exception('Main', f'Unknown exception caught in main loop:', e)
            errors.append(f'Unknown exception caught in main loop: {traceback.format_exc()}')

    return errors


# still not 100% sure what this does, but it looks important
if __name__ == "__main__":
    lambda_handler(None, None)
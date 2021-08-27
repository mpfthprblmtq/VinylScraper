# imports
import time
import logging

from objects.found import Found
from services.email_service import EmailService
from services.reddit_service import RedditService
from services.alert_service import AlertService
from services.uptime_service import UptimeService
from services.post_analyzer_service import PostAnalyzerService

# globals
app_info = []
keyword_list = []
SLEEP_INTERVAL_M = 10

# logging config
LOGGING_LEVEL = logging.INFO
FORMAT = '[%(asctime)s] %(levelname)-7s %(message)s'
logging.basicConfig(level=LOGGING_LEVEL, format=FORMAT, filename='log.log')


# cleans the string
def clean_string(s, start_index):
    s = s.replace('\n', '')
    s = s[start_index:len(s)]
    return s


# custom pretty print function to return a nice string representation of an array
def prettify_array(arr):
    res = ""
    for e in arr:
        res += e + ", "
    res = res[0: len(res) - 2]
    return res


# reads in the app info
def read_app_info():
    global app_info  # get the global

    f = open('app_info.txt', 'r')
    client_id = clean_string(f.readline(), 10)
    client_secret = clean_string(f.readline(), 14)
    user_agent = clean_string(f.readline(), 11)
    sender_email = clean_string(f.readline(), 13)
    receiving_email = clean_string(f.readline(), 16)
    sender_email_password = clean_string(f.readline(), 22)
    subreddits = clean_string(f.readline(), 11)
    app_info = [client_id, client_secret, user_agent, sender_email, receiving_email, sender_email_password, subreddits]


# reads in the keywords.txt file to get all the words to look out for
def read_keywords():
    global keyword_list  # get the global

    f = open('keywords.txt', 'r')
    for line in f:
        keyword_list.append(clean_string(line, 0))


def main():
    # populate globals
    read_app_info()
    read_keywords()

    # initialize services
    global app_info
    global keyword_list
    uptime_service = UptimeService(time.time())  # populates the uptime service with the current time for start time
    reddit_service = RedditService(app_info[0], app_info[1], app_info[2])
    email_service = EmailService(app_info[4], app_info[3], app_info[5], app_info[2], uptime_service)
    alert_service = AlertService()
    post_analyzer_service = PostAnalyzerService(keyword_list)

    # send startup notification
    email_service.send_startup_email()

    # get the subreddits we want to search for
    subreddits = app_info[6].split(',')

    # do the loop de loop
    while True:
        try:
            # traverse through the subreddits in app_info
            for subreddit in subreddits:
                # get the posts
                posts = reddit_service.get_new_posts(subreddit, 10)
                # traverse through all the posts we got
                for post in posts:
                    # check to see if we found a match (or matches)
                    found_keywords = post_analyzer_service.find_keyword(post.title, post.selftext)
                    if found_keywords:
                        if alert_service.should_alert(found_keywords, post.title):
                            # log what we found
                            logging.info(f"{'Main'.ljust(18)} : Match found ({prettify_array(found_keywords)}), "
                                         f"sending email!")
                            # send the match email
                            email_service.send_match_email(prettify_array(found_keywords), post)
                            # put all matched keywords in the already alerted array
                            for keyword in found_keywords:
                                alert_service.already_alerted.append(Found(keyword, time.time()))

            # sleepy sleep
            logging.info(f"{uptime_service.get().ljust(18)} : Sleeping for {SLEEP_INTERVAL_M} minutes...")
            time.sleep(SLEEP_INTERVAL_M * 60)
        except Exception as e:
            if e.response.status_code == 401:
                # check if it's a 401, which is probably just a config issue
                logging.error(f'Received a 401 response code from reddit')
                email_service.send_shutdown_email(e)
                time.sleep(10)
                quit()
            elif e.response.status_code == 503:
                # check if it's a 503, which means reddit is down
                logging.error(f'Received a 503 response code from reddit')
                # we just want to continue in this case, because reddit will be up again soon... right?
            else:
                logging.error(f'Unknown exception caught in main loop:')
                logging.error(f'{e}')
                email_service.send_shutdown_email(e)
                time.sleep(10)
                quit()


if __name__ == "__main__":
    main()

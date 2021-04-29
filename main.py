# imports
import time
import logging

from objects.found import Found
from services.email_service import EmailService
from services.reddit_service import RedditService
from services.alert_service import AlertService


# globals
app_info = []
keyword_list = []
SLEEP_INTERVAL_M = 5

# logging config
LOGGING_LEVEL = logging.INFO
FORMAT = '[%(asctime)s] %(levelname)-7s %(message)s'
logging.basicConfig(level=LOGGING_LEVEL, format=FORMAT)


# cleans the string
def clean_string(s, start_index):
    s = s.replace('\n', '')
    s = s[start_index:len(s)]
    return s


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


# looks for any keyword in the title or description of the post
def find_keyword(title, description):
    global keyword_list
    for keyword in keyword_list:
        if keyword in title:
            return keyword
        if description != '':
            if keyword in description:
                return keyword


def get_uptime(start_time):
    uptime_seconds = time.time() - start_time
    uptime_h = uptime_seconds // 3600
    uptime_m = uptime_seconds // 60
    if uptime_h > 0:
        uptime_m = uptime_m - (uptime_h * 60)

    uptime_s = uptime_seconds - (uptime_m * 60)
    return str(int(uptime_h)) + "h " + str(int(uptime_m)) + "m " + str(int(uptime_s)) + "s"


def main():
    # populate globals
    read_app_info()
    read_keywords()

    # initialize services
    global app_info
    reddit_service = RedditService(app_info[0], app_info[1], app_info[2])
    email_service = EmailService(app_info[4], app_info[3], app_info[5])
    alert_service = AlertService()

    # get the start time
    start_time = time.time()

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
                    # check to see if we found a match
                    found_keyword = find_keyword(post.title, post.selftext)
                    if found_keyword is not None:
                        if alert_service.should_alert(found_keyword, post.title):
                            logging.info(f"{'Main()'.ljust(15)} : Match found ({found_keyword}), sending email!")
                            email_service.send_email(found_keyword, post)
                            alert_service.already_alerted.append(Found(found_keyword, time.time()))

            # sleepy sleep
            logging.info(f"{get_uptime(start_time).ljust(15)} : Sleeping for {SLEEP_INTERVAL_M} minutes...")
            time.sleep(SLEEP_INTERVAL_M * 60)
        except Exception as e:
            logging.error(f'Exception caught in main loop:\n{e}')
            logging.error(f'{e.with_traceback()}')
            quit()


if __name__ == "__main__":
    main()

# imports
import smtplib
import ssl
import time
import logging
import praw

from email.mime.text import MIMEText


# class used to store the keyword and time found for alerting
class Found:
    def __init__(self, keyword, time_found):
        self.keyword = keyword
        self.time_found = time_found


# globals
app_info = []
keyword_list = []
already_alerted = []
SLEEP_INTERVAL_S = 300
ALERT_COOLDOWN_S = 3600

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
    app_info = [client_id, client_secret, user_agent, sender_email, receiving_email, sender_email_password]


# reads in the keywords.txt file to get all the words to look out for
def read_keywords():
    global keyword_list  # get the global

    f = open('keywords.txt', 'r')
    for line in f:
        keyword_list.append(clean_string(line, 0))


# actually makes the call to reddit
def make_call(reddit, subreddit):
    return reddit.subreddit(subreddit).new(limit=10)


# looks for any keyword in the title of the post
def find_keyword(title, keywords):
    for keyword in keywords:
        if keyword in title:
            return keyword


def has_already_alerted(keyword):
    global already_alerted
    for x in already_alerted:
        if x.keyword == keyword:
            return x
    return None


# checks to see if we've already alerted
def should_alert(keyword):
    global already_alerted
    x = has_already_alerted(keyword)    # check to see if we've already sent an alert on this
    if x is not None:
        # we have already alerted, check if we're in the cooldown
        if time.time() - x.time_found > ALERT_COOLDOWN_S:
            # we are outside of the cooldown period
            already_alerted.remove(x)
            return True
        else:
            return False
    else:
        # keyword wasn't in the already_alerted array, we should alert
        return True


# sends the email
def send_email(keyword, reddit_post):
    global app_info
    sender_email = app_info[3]
    receiver_email = app_info[4]
    sender_email_password = app_info[5]

    port = 465
    context = ssl.create_default_context()
    msg_text = f"""\
VinylScraper is doing its job!  Found a post:

Post title: {reddit_post.title}

Url in post: {reddit_post.url}"""

    msg = MIMEText(msg_text)
    msg['Subject'] = f'VinylScraper: Match found! ({keyword})'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
        server.login(sender_email, sender_email_password)
        server.sendmail(sender_email, [receiver_email], msg.as_string())
        logging.info(f'Successfully sent email on match: {keyword}')


def get_uptime(start_time):
    uptime_seconds = time.time() - start_time
    uptime_h = uptime_seconds // 3600
    uptime_m = uptime_seconds // 60
    uptime_s = uptime_seconds - (uptime_m * 60)
    return str(int(uptime_h)) + "h " + str(int(uptime_m)) + "m " + str(int(uptime_s)) + "s"


def main():
    # populate globals
    read_app_info()
    read_keywords()
    global already_alerted

    # create reddit instance
    reddit = praw.Reddit(
        client_id=app_info[0],
        client_secret=app_info[1],
        user_agent=app_info[2])

    # get the start time
    start_time = time.time()

    # do the loop de loop
    while True:
        try:
            posts = make_call(reddit, 'VinylReleases')
            for post in posts:
                found_keyword = find_keyword(post.title, keyword_list)

                # check to see if we found a match
                if found_keyword is not None:
                    if should_alert(found_keyword):
                        logging.info(f"Match found ({found_keyword}), sending email!")
                        send_email(found_keyword, post)
                        already_alerted.append(Found(found_keyword, time.time()))

            # sleepy sleep
            logging.info(f"{get_uptime(start_time).ljust(15)} : Sleeping for {SLEEP_INTERVAL_S} seconds...")
            time.sleep(SLEEP_INTERVAL_S)
        except Exception as e:
            logging.error(f'Exception caught in main loop:\n{e}')
            quit()


if __name__ == "__main__":
    main()

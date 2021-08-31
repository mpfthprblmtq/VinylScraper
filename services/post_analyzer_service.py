import time
from objects.found_item import FoundItem
from utils.string_utils import string_found, remove_duplicates, prettify_array


# finds the keyword
# looks for any keyword in the title or description of the post
def find_keyword(title, description, keywords):
    found_keywords = []
    for keyword in keywords:
        if string_found(keyword, title):
            found_keywords.append(keyword)
        if description != '':
            if string_found(keyword, description):
                found_keywords.append(keyword)
    return remove_duplicates(found_keywords)


class PostAnalyzerService:

    def __init__(self, reddit_service, alert_service, email_service, logger):
        self.reddit_service = reddit_service
        self.alert_service = alert_service
        self.email_service = email_service
        self.logger = logger

    # analyzes the posts
    # for each subreddit
    def analyze_posts(self, user):
        # traverse the subreddits to search
        for subreddit in user.subreddits:
            # get the posts from that subreddit
            posts = self.reddit_service.get_new_posts(subreddit, 10)
            # traverse through all the posts we got
            for post in posts:
                # check to see if we found a match (or matches)
                found_keywords = find_keyword(post.title, post.selftext, user.keywords)
                if found_keywords:
                    # check to see if we should alert
                    if self.alert_service.should_alert_on_reddit_post(found_keywords, post.title):
                        # log what we found
                        self.logger.info('PostService', f'Match found ({prettify_array(found_keywords)}), sending email!')
                        # send the match email
                        self.email_service.send_reddit_match_email(prettify_array(found_keywords), post, user)
                        # put all matched keywords in the already alerted array
                        for keyword in found_keywords:
                            self.alert_service.already_alerted_reddit.append(FoundItem(keyword, time.time()))

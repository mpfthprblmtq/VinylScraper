# imports
import praw
import time
from _objects.found_item import FoundItem
from _utils.string_utils import string_found, remove_duplicates, prettify_array


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


# service class that calls reddit
class RedditService:

    def __init__(self, client_id, client_secret, user_agent, alert_service, email_service, logger):
        # create reddit instance
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent)
        self.alert_service = alert_service
        self.email_service = email_service
        self.logger = logger

    # actually makes the call to reddit for new posts
    #   subreddit: the subreddit to query
    #   post_count: the number of posts to limit to
    def get_new_posts(self, subreddit, post_count):
        return self.reddit.subreddit(subreddit).new(limit=post_count)

    # actually makes the call to reddit for hot posts
    #   subreddit: the subreddit to query
    #   post_count: the number of posts to limit to
    def get_hot_posts(self, subreddit, post_count):
        return self.reddit.subreddit(subreddit).hot(limit=post_count)

    # analyzes the posts for each subreddit
    #   user: the user to search for
    def analyze_posts(self, user):
        # traverse the subreddits to search
        for subreddit in user.subreddits:
            self.logger.info('RedditService', f'Searching subreddit r/{subreddit}')
            # get the posts from that subreddit
            posts = self.get_new_posts(subreddit, 10)
            # traverse through all the posts we got
            for post in posts:
                # check to see if we found a match (or matches)
                found_keywords = find_keyword(post.title, post.selftext, user.reddit_keywords)
                if found_keywords:
                    # check to see if we should alert
                    if self.alert_service.should_alert(post.id, 'reddit'):
                        # log what we found
                        self.logger.info('RedditService',
                                         f'Match found ({prettify_array(found_keywords)}), sending email!')
                        # send the match email
                        self.email_service.send_reddit_match_email(prettify_array(found_keywords), post, user)
                        # put the post id in the already alerted array
                        self.alert_service.add_found_item_to_list(FoundItem('reddit', post.id, time.time()))

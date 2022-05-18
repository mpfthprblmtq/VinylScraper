# utils
from _utils.string_utils import join_email


# class used to store user information
class User:
    def __init__(self, username, emails, urls, reddit_dict, twitter_profiles):
        self.username = username
        self.emails = join_email(emails)
        self.urls = urls
        self.subreddits = reddit_dict['subreddits']
        self.reddit_keywords = reddit_dict['keywords']
        self.twitter_profiles = twitter_profiles

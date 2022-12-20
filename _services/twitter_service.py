# imports
import time
import tweepy
from _utils.string_utils import string_found, remove_duplicates, prettify_array
from _objects.found_item import FoundItem


def find_keyword(keywords, tweet_text):
    found_keywords = []
    for keyword in keywords:
        if string_found(keyword, tweet_text):
            found_keywords.append(keyword)
    return remove_duplicates(found_keywords)


# service class that calls twitter
class TwitterService:

    def __init__(self, bearer_token, email_service, alert_service, logger):
        # create api instance
        self.client = tweepy.Client(bearer_token=bearer_token)
        self.email_service = email_service
        self.alert_service = alert_service
        self.logger = logger

    # actually makes the call to twitter for recent tweets by the given user
    #   handle: the user's @profile to get tweets from
    def get_recent_posts(self, handle):
        query = f'from:{handle}'
        return self.client.search_recent_tweets(query=query, max_results=10)

    # searches for tweets using the user's parameters
    #   user: the user with the twitter information
    def search_tweets(self, user):
        # traverse the twitter profiles to search on
        for twitter_profile in user.twitter_profiles:
            self.logger.info('TwitterService', f'Searching for tweets from {twitter_profile.name} (@{twitter_profile.handle})')
            # get the 10 most recent tweets from that user
            tweets = self.get_recent_posts(twitter_profile.handle)
            # if we get tweets back (account could be private)
            if tweets.data:
                # traverse through all the tweets we got
                for tweet in tweets.data:
                    # check to see if we found a match
                    found_keywords = find_keyword(twitter_profile.keywords, tweet.text)
                    if found_keywords:
                        # check to see if we should alert
                        if self.alert_service.should_alert(tweet.id, 'twitter'):
                            # log what we found
                            self.logger.info('TwitterService',
                                             f'Match found ({prettify_array(found_keywords)}), sending email!')
                            # send the match email
                            self.email_service.send_twitter_match_email(prettify_array(found_keywords), tweet, twitter_profile.handle, user)
                            # put the tweet in the already alerted array
                            self.alert_service.add_found_item_to_list(FoundItem('twitter', tweet.id, time.time()))

# imports
import time
import json
import boto3
from _objects.found_item import FoundItem
from datetime import datetime


# checks the list of FoundItems given to see if the item with that keyword exists in the list
#   keyword: the keyword to look for
#   alerted_list: the list of FoundItems to search
def has_already_alerted(keyword, alerted_list):
    for x in alerted_list:
        if x.keyword == keyword:
            return x
    return None


# service class that keeps track of things we've already alerted on
class AlertService:
    already_alerted = []

    ALERT_COOLDOWN_REDDIT_S = 21600  # 6 hours
    ALERT_COOLDOWN_PAGE_SEARCH_S = 21600  # 6 hours
    ALERT_COOLDOWN_TWITTER_S = 604800  # 7 days
    PURGE_WINDOW_S = 2629746  # one(ish) month

    # S3 configuration
    BUCKET_NAME = 'vinyl-scraper-bucket'
    KEY = 'already_alerted.json'
    S3 = boto3.client('s3')

    def __init__(self, logger):
        self.logger = logger
        self.get_all_already_alerted()
        # self.log_already_alerted()
        self.purge_already_alerted()
        # pass

    # def log_already_alerted(self):
    #     msg = 'Already alerted items:\n'
    #     for item in self.already_alerted:
    #         msg += item.found_type + ', '
    #         msg += str(item.keyword) + ', '
    #         msg += str(datetime.fromtimestamp(item.time_found))
    #         msg += '\n'

    # purges all already found elements older than one month
    def purge_already_alerted(self):
        for item in self.already_alerted:
            if time.time() - item.time_found > self.PURGE_WINDOW_S:
                self.already_alerted.remove(item)
        self.write_all_already_alerted()

    # gets all elements in the already alerted file
    def get_all_already_alerted(self):
        # load from S3
        response = self.S3.get_object(Bucket=self.BUCKET_NAME, Key=self.KEY)
        content = response['Body']
        # get json
        json_data = json.loads(content.read())
        # populate lists
        for item in json_data:
            self.already_alerted.append(FoundItem(item['found_type'], item['keyword'], item['time_found']))

    # writes all the already alerted lists and uploads it to S3
    def write_all_already_alerted(self):
        json_data = [ob.__dict__ for ob in self.already_alerted]
        upload_byte_stream = bytes(json.dumps(json_data).encode('UTF-8'))
        self.S3.put_object(Bucket=self.BUCKET_NAME, Key=self.KEY, Body=upload_byte_stream)

    # adds found item to designated list
    #   found_item: the FoundItem to add
    def add_found_item_to_list(self, found_item):
        self.already_alerted.append(found_item)
        self.write_all_already_alerted()

    # return the cooldown based on the context we're currently in using a dictionary
    def get_cooldown(self, context):
        return {
            'reddit': self.ALERT_COOLDOWN_REDDIT_S,
            'twitter': self.ALERT_COOLDOWN_TWITTER_S,
            'pages': self.ALERT_COOLDOWN_PAGE_SEARCH_S
        }.get(context)

    def should_alert(self, key, context):
        # get the cooldown
        cooldown = self.get_cooldown(context)
        # check to see if we've already sent an alert on this
        x = has_already_alerted(key, self.already_alerted)
        if x is not None:
            # we have already alerted, check if we're in the cooldown
            if time.time() - x.time_found > cooldown:
                # we are outside the cooldown period
                # remove the old already alerted item from the list
                self.already_alerted.remove(x)
                return True
            else:
                # we are still in the cooldown period, don't alert just yet
                return False
        else:
            # keyword wasn't in the __already_alerted array, we should alert
            return True

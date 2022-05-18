# utils
from _utils.string_utils import join_email
import json


# object used to define app information
# reads the app_info.json file and uses json to populate itself
# check out the readme for more detailed information
class AppInfo:

    def __init__(self):
        # get all the json data in the file
        f = open('app_info.json')
        json_data = json.load(f)

        # populate fields
        self.reddit_client_id = json_data['reddit_client_id']
        self.reddit_client_secret = json_data['reddit_client_secret']
        self.twitter_bearer_token = json_data['twitter_bearer_token']
        self.user_agent = json_data['user_agent']
        self.sender_email = join_email([json_data['sender_email']])[0]
        self.sender_email_password = json_data['sender_email_password']
        self.maintenance_email = join_email([json_data['maintenance_email']])[0]

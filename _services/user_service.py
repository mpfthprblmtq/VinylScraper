# imports
from os import listdir
from os.path import isfile, join
import json

# _objects
from _objects.search_url import SearchUrl
from _objects.user import User
from _objects.twitter_profile import TwitterProfile


# service class that allows us to keep track of __users within the app
class UserService:

    # __init__
    def __init__(self):
        self.path = './__users/'  # the folder that contains the user files
        self.users = []
        self.init_users()   # init the __users

    # inits the __users
    # scans the __users directory and reads in those text files
    def init_users(self):
        # subscribe to my only_files
        only_files = [f for f in listdir(self.path) if isfile(join(self.path, f))]
        for file in only_files:
            # get all the json data in the file
            f = open(self.path + file)
            json_data = json.load(f)
            # extract data into vars
            username = json_data['user_info']['username']
            emails = json_data['user_info']['emails']
            urls = []
            for url in json_data['urls']:
                urls.append(SearchUrl(url))
            reddit_dict = json_data['reddit']
            twitter_profiles = []
            for twitter_profile in json_data['twitter']:
                twitter_profiles.append(TwitterProfile(twitter_profile['handle'], twitter_profile['keywords']))
            self.users.append(User(
                username,
                emails,
                urls,
                reddit_dict,
                twitter_profiles
            ))

    # returns the __users array
    def get_users(self):
        return self.users

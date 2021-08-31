# imports
from os import listdir
from os.path import isfile, join

# objects
from objects.search_url import SearchUrl
from objects.user import User

# utils
from utils.string_utils import clean_string


# returns a SearchUrl object by splitting the string given on a comma
#   s: the string to split
def get_url(s):
    arr = s.split(',')
    return SearchUrl(arr[0], arr[1], arr[2])


# service class that allows us to keep track of users within the app
class UserService:

    # __init__
    def __init__(self):
        self.path = './users/'  # the folder that contains the user files
        self.users = []
        self.init_users()   # init the users

    # inits the users
    # scans the users directory and reads in those text files
    def init_users(self):
        # subscribe to my only_files
        only_files = [f for f in listdir(self.path) if isfile(join(self.path, f))]
        for file in only_files:
            username = ''
            email = ''
            urls = []
            subreddits = []
            keywords = []
            with open(self.path + file) as f:
                lines = f.readlines()
                lines = [line.rstrip() for line in lines]
                for line in lines:
                    # skip any lines that start with # (comments)
                    if not line.startswith('#'):
                        if line.startswith('username='):
                            username = clean_string(line, 9)
                        elif line.startswith('email='):
                            email = clean_string(line, 6)
                        elif line.startswith('url='):
                            line_content = clean_string(line, 4)
                            if line_content != '':
                                urls.append(get_url(line_content))
                        elif line.startswith('subreddits='):
                            line_content = clean_string(line, 11)
                            if line_content != '':
                                subreddits = line_content.split(',')
                        else:
                            if line != '' and line != 'keywords=':
                                keywords.append(line)

                # create a new user object and add it to the main list of users
                self.users.append(User(username, email, urls, subreddits, keywords))

    # returns the users array
    def get_users(self):
        return self.users

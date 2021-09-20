# objects
from objects.search_url import SearchUrl

# utils
from utils.string_utils import join_email


# returns a list in json style
#   arr: the array of items
#   space: the spacing to put before each item (usually one or multiple \t characters)
#   end_space: the spacing to put on the last line (usually one less \t character than the space parameter)
def get_json_array(arr, space, end_space):
    s = ''
    if len(arr) == 0:
        return s

    if type(arr[0]) == SearchUrl:
        for e in arr:
            s = s + '\n' + space + '{' + e.url + ', ' + e.search_string + '}'
    else:
        for e in arr:
            s = s + '\n' + space + e
    s = s + '\n' + end_space
    return s


# class used to store user information
class User:
    def __init__(self, username, email, urls, subreddits, keywords):
        self.username = username
        self.emails = join_email(email)
        self.urls = urls
        self.subreddits = subreddits
        self.keywords = keywords

    # prints a nice json representation of the object because I didn't want to deal with making the object serializable
    # why use libraries when I can just spend my own precious time hard coding everything?
    def to_string(self):
        return 'User: {\n' + \
               '\tusername: ' + self.username + \
               '\n\temail: ' + self.emails + \
               '\n\turls: [' + get_json_array(self.urls, '\t\t', '\t') + ']' + \
               '\n\tsubreddits: [' + get_json_array(self.subreddits, '\t\t', '\t') + ']' + \
               '\n\tkeywords: [' + get_json_array(self.keywords, '\t\t', '\t') + ']' + \
               '\n}'

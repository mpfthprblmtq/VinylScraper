from objects.search_url import SearchUrl
from utils.string_utils import join_email


# returns a list in json style
def get_json_array(arr, space, end_space):
    s = ''
    if len(arr) == 0:
        return s

    if type(arr[0]) == SearchUrl:
        for e in arr:
            s = s + '\n' + space + '{' + e.url + ', ' + e.search + '}'
    else:
        for e in arr:
            s = s + '\n' + space + e
    s = s + '\n' + end_space
    return s


# class used to store user information
class User:
    def __init__(self, username, email, urls, subreddits, keywords):
        self.username = username
        self.email = join_email(email)
        self.urls = urls
        self.subreddits = subreddits
        self.keywords = keywords

    def to_string(self):
        return 'User: {\n' + \
            '\tusername: ' + self.username + \
            '\n\temail: ' + self.email + \
            '\n\turls: [' + get_json_array(self.urls, '\t\t', '\t') + ']' + \
            '\n\tsubreddits: [' + get_json_array(self.subreddits, '\t\t', '\t') + ']' + \
            '\n\tkeywords: [' + get_json_array(self.keywords, '\t\t', '\t') + ']' + \
            '\n}'

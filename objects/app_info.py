# utils
from utils.string_utils import clean_string, join_email


# object used to define app information
# reads the app_info.txt file and uses some string utilities to populate itself
# check out the readme for more detailed information
class AppInfo:

    def __init__(self):
        f = open('app_info.txt', 'r')
        self.client_id = clean_string(f.readline(), 10)
        self.client_secret = clean_string(f.readline(), 14)
        self.user_agent = clean_string(f.readline(), 11)
        self.sender_email = join_email(clean_string(f.readline(), 13))[0]
        self.sender_email_password = clean_string(f.readline(), 22)
        self.maintenance_email = join_email(clean_string(f.readline(), 18))[0]

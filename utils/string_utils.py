# imports
import re


# cleans the string by getting rid of newlines and performing a pseudo substring
#   s: the string to clean
def clean_string(s, start_index):
    s = s.replace('\n', '')
    s = s[start_index:len(s)]
    return s


# custom pretty print function to return a nice string representation of an array
#   arr: the array to prettify
def prettify_array(arr):
    res = ''
    for e in arr:
        res += e + ', '
    res = res[0: len(res) - 2]
    return res


# uses regex to find the string in a word format
#   string_to_find: the string to find
#   string to search: the string to search in
def string_found(string_to_find, string_to_search):
    if re.search(r'\b' + re.escape(string_to_find.lower()) + r'\b', string_to_search.lower()):
        return True
    return False


# custom duplicate removal function
#   arr: the array to check for duplicates in
def remove_duplicates(arr):
    res = []
    for e in arr:
        if e not in res:
            res.append(e)
    return res


# joins a string representation of an email into an actual email
#   email: the string to split into the email
def join_email(email):
    emails = []
    emails_arr = email.split(',')
    for e in emails_arr:
        arr = e.split('/')
        if len(arr) == 3:
            emails.append(arr[0] + '@' + arr[1] + '.' + arr[2])
    return emails

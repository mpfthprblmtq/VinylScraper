import re


# cleans the string
def clean_string(s, start_index):
    s = s.replace('\n', '')
    s = s[start_index:len(s)]
    return s


# custom pretty print function to return a nice string representation of an array
def prettify_array(arr):
    res = ""
    for e in arr:
        res += e + ", "
    res = res[0: len(res) - 2]
    return res


# uses regex to find the string in a word format
def string_found(string_to_find, string_to_search):
    if re.search(r"\b" + re.escape(string_to_find.lower()) + r"\b", string_to_search.lower()):
        return True
    return False


# custom duplicate removal function
def remove_duplicates(arr):
    res = []
    for e in arr:
        if e not in res:
            res.append(e)
    return res


# used to join the email by delimiting it with commas
def join_email(email):
    arr = email.split(',')
    if len(arr) == 3:
        return arr[0] + '@' + arr[1] + '.' + arr[2]
    return email

import re


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


class PostAnalyzerService:

    def __init__(self, keyword_list):
        self.keyword_list = keyword_list

    # looks for any keyword in the title or description of the post
    def find_keyword(self, title, description):
        found_keywords = []
        for keyword in self.keyword_list:
            if string_found(keyword, title):
                found_keywords.append(keyword)
            if description != '':
                if string_found(keyword, description):
                    found_keywords.append(keyword)
        return remove_duplicates(found_keywords)

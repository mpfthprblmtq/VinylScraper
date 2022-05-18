# class used to store the keyword and time found for alerting
class FoundItem:
    def __init__(self, found_type, keyword, time_found):
        self.found_type = found_type
        self.keyword = keyword
        self.time_found = time_found

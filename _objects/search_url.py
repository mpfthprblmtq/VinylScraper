# class used to store the url, string to search, and actual product
class SearchUrl:
    def __init__(self, url_dict):
        self.url = url_dict['url']
        self.keyword = url_dict['keyword']
        self.product = url_dict['product']

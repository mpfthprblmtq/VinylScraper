# imports
import urllib.request


# gets the page content from the given url
# returns a squished version of the html (single line, no spaces) to prevent any weird spacing/tab issues
#   url: the url to search
def get_page_content(url):
    fp = urllib.request.urlopen(url)    # open the connection
    content_bytes = fp.read()
    content = content_bytes.decode('utf8')
    fp.close()  # close the connection

    # now lets split join that string so we can search it better
    squished_content = ''.join(str(content).split())
    return squished_content


# looks for the text in the page content by squishing the search criteria
#   page_content: the raw html of the page
#   search_string: the string to search for
def find_keyword(page_content, search_string):
    return ''.join(str(search_string)).upper() in str(page_content).upper()


# service class that allows us to search html pages for certain phrases
class PageSearchService:

    # init
    def __init__(self, alert_service, email_service):
        self.alert_service = alert_service
        self.email_service = email_service

    # analyzes the pages
    # gets the page content, then checks if the keyword/key phrase exists in the page
    #   user: the user with the urls to search for
    def analyze_pages(self, user):
        for search_url in user.urls:
            content = get_page_content(search_url.url)
            if find_keyword(content, search_url.search_string):
                self.email_service.send_page_match_email(search_url, user)

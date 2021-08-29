import urllib.request


# gets the page content
# but squishes it first to prevent any weird spacing/tab issues
def get_page_content(url):
    fp = urllib.request.urlopen(url)
    content_bytes = fp.read()
    content = content_bytes.decode('utf8')
    fp.close()

    # now lets split that string so we can search it better
    squished_content = ''.join(str(content).split())
    return squished_content


# looks for the text in the page content
def find_keyword(page_content, search_string):
    return ''.join(str(search_string)).upper() in str(page_content).upper()


class PageSearchService:

    # init
    def __init__(self, alert_service, email_service):
        self.alert_service = alert_service
        self.email_service = email_service

    # analyzes the pages
    # gets the page content, then checks if the keyword/keyphrase exists in the page
    def analyze_pages(self, user):
        for search_url in user.urls:
            content = get_page_content(search_url.url)
            if find_keyword(content, search_url.search):
                self.email_service.send_page_match_email(search_url, user)

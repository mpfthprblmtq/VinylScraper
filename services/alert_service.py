import time


# checks the list given to see if the keyword exists in the list
def has_already_alerted(keyword, alerted_list):
    for x in alerted_list:
        if x.keyword == keyword:
            return x
    return None


class AlertService:
    already_alerted_reddit = []
    already_alerted_pages = []
    ALERT_COOLDOWN_S = 21600

    def __init__(self):
        pass

    # checks to see if we've already alerted or if we should alert
    # for reddit posts
    def should_alert_on_reddit_post(self, keywords, title):

        # we don't want any vinyl collectors posts containing [Wanted]
        if '[Wanted]'.upper() in str(title).upper():
            return False

        should_alert = False
        for keyword in keywords:
            # check to see if we've already sent an alert on this
            x = has_already_alerted(keyword, self.already_alerted_reddit)
            if x is not None:
                # we have already alerted, check if we're in the cooldown
                if time.time() - x.time_found > self.ALERT_COOLDOWN_S:
                    # we are outside of the cooldown period
                    self.already_alerted_reddit.remove(x)
                    should_alert = True
                else:
                    # we are still in the cooldown period, don't alert just yet
                    should_alert = False
            else:
                # keyword wasn't in the already_alerted array, we should alert
                should_alert = True
        return should_alert

    # checks to see if we've already alerted or if we should alert
    # for web page searches
    def should_alert_on_page_search(self, url):
        should_alert = False
        x = has_already_alerted(url, self.already_alerted_pages)
        if x is not None:
            # we have already alerted, check if we're in the cooldown period
            if time.time() - x.time_found > self.ALERT_COOLDOWN_S:
                # we are outside the cooldown period, send out the alert
                self.already_alerted_pages.remove(x)
                should_alert = True
            else:
                # we are still in the cooldown period, don't alert just yet
                should_alert = False
        else:
            # url wasn't in the already_alerted array, we should alert
            should_alert = True
        return should_alert

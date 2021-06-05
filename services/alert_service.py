import time


class AlertService:
    already_alerted = []
    ALERT_COOLDOWN_S = 14400

    def __init__(self):
        pass

    def has_already_alerted(self, keyword):
        for x in self.already_alerted:
            if x.keyword == keyword:
                return x
        return None

    # checks to see if we've already alerted
    # or if we should alert
    def should_alert(self, keywords, title):

        # we don't want any vinyl collectors posts starting with [Wanted]
        if str(title).startswith('[Wanted]'):
            return False

        should_alert = False
        for keyword in keywords:
            x = self.has_already_alerted(keyword)  # check to see if we've already sent an alert on this
            if x is not None:
                # we have already alerted, check if we're in the cooldown
                if time.time() - x.time_found > self.ALERT_COOLDOWN_S:
                    # we are outside of the cooldown period
                    self.already_alerted.remove(x)
                    should_alert = True
                else:
                    # we are still in the cooldown period, don't alert just yet
                    should_alert = False
            else:
                # keyword wasn't in the already_alerted array, we should alert
                should_alert = True
        return should_alert

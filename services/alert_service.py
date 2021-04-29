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
    def should_alert(self, keyword, title):

        # we don't want any vinyl collectors posts starting with [Wanted]
        if str(title).startswith('[Wanted]'):
            return False

        x = self.has_already_alerted(keyword)  # check to see if we've already sent an alert on this
        if x is not None:
            # we have already alerted, check if we're in the cooldown
            if time.time() - x.time_found > self.ALERT_COOLDOWN_S:
                # we are outside of the cooldown period
                self.already_alerted.remove(x)
                return True
            else:
                return False
        else:
            # keyword wasn't in the already_alerted array, we should alert
            return True

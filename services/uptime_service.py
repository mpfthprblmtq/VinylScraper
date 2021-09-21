# imports
import time


# service class that lets us control the uptime
class UptimeService:

    # init
    def __init__(self, start_time):
        self.start_time = start_time

    # returns the uptime in ##d ##h ##m ##s format
    def get(self):
        uptime_seconds = int(time.time() - self.start_time)
        uptime_d = int(uptime_seconds // 86400)
        uptime_h = int(uptime_seconds // 3600)
        uptime_m = int(uptime_seconds // 60)
        uptime_s = int(uptime_seconds)

        # do some modulus
        if uptime_s >= 60:
            uptime_s = uptime_s % 60
        if uptime_m >= 60:
            uptime_m = uptime_m % 60
        if uptime_h >= 24:
            uptime_h = uptime_h % 24

        # make a string
        formatted_string = str(uptime_d) + "d " + str(uptime_h) + "h " + str(uptime_m) + "m " + str(uptime_s) + "s"
        return formatted_string

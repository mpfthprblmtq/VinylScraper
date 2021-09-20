# imports
import time


# service class that lets us control the uptime
class UptimeService:

    # init
    def __init__(self, start_time):
        self.start_time = start_time

    # returns the uptime in ##d ##h ##m ##s format
    def get(self):
        uptime_seconds = time.time() - self.start_time
        uptime_d = uptime_seconds // 86400
        uptime_h = uptime_seconds // 3600
        uptime_m = uptime_seconds // 60
        if uptime_d > 0:
            uptime_h = uptime_h - (uptime_d * 24)
        if uptime_h > 0:
            uptime_m = uptime_m - (uptime_h * 60)

        uptime_s = uptime_seconds - ((uptime_d * 86400) + (uptime_m * 60) + (uptime_h * 3600))
        return \
            str(int(uptime_d)) + "d " + str(int(uptime_h)) + "h " + str(int(uptime_m)) + "m " + str(int(uptime_s)) + "s"

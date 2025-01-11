import math
from datetime import datetime

interval = 60 + 1  # with margin

class APILimiter:
    def __init__(self, rpm = None):
        self.list = []
        self.rpm = rpm  # requests per minute

    def done(self, time=None):
        if time is None:
            time = datetime.now()
        self.list.append(time)

    def check_wait(self, time=None):
        if self.rpm and len(self.list) >= self.rpm:
            if time is None:
                time = datetime.now()
            t = (time - self.list[-self.rpm]).total_seconds()
            if t <= interval:
                return math.ceil((interval - t) * 10) / 10
        return 0

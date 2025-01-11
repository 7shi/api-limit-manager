import math, uuid
from datetime import datetime

interval = 60 + 1  # with margin

class APILimiter:
    def __init__(self, rpm = None):
        self.list = []
        self.rpm = rpm  # requests per minute
        self.last_uuid = None

    def start(self):
        self.last_uuid = str(uuid.uuid4())
        return self.last_uuid

    def done(self, uid=None, time=None):
        if uid is None:
            uid = self.last_uuid
            if uid is None:
                raise Exception("Not started.")
        if time is None:
            time = datetime.now()
        self.list.append((uid, time))
        self.last_uuid = None

    def check_wait(self, time=None):
        if self.rpm and len(self.list) >= self.rpm:
            if time is None:
                time = datetime.now()
            t = (time - self.list[-self.rpm][1]).total_seconds()
            if t <= interval:
                return math.ceil((interval - t) * 10) / 10
        return 0

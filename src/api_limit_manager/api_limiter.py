import math, uuid
from datetime import datetime
from .backend_list import BackendList

interval = 60 + 1  # with margin

class APILimiter:
    def __init__(self, rpm = None):
        self.list = BackendList()
        self.rpm = rpm  # requests per minute
        self.last_uuid = None

    def start(self, start_time=None):
        if start_time is None:
            start_time = datetime.now()
        self.last_uuid = str(uuid.uuid4())
        self.list.start(self.last_uuid, start_time)
        return self.last_uuid

    def done(self, uid=None, end_time=None):
        if uid is None:
            uid = self.last_uuid
            if uid is None:
                raise Exception("Not started.")
        if end_time is None:
            end_time = datetime.now()
        self.list.done(uid, end_time)
        self.last_uuid = None

    def check_wait(self, time=None):
        end_time = self.list.get_time(self.rpm)
        if end_time:
            if time is None:
                time = datetime.now()
            t = (time - end_time).total_seconds()
            if t <= interval:
                return math.ceil((interval - t) * 10) / 10
        return 0

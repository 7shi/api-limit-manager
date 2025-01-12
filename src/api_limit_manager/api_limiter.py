import math, uuid
from datetime import datetime
from multiprocessing import Lock
from .backend_list import BackendList

interval = 60 + 1  # with margin

class APILimiter:
    _global_lock = Lock()

    def __init__(self, rpm = None):
        self.list = BackendList()
        self.rpm = rpm  # requests per minute
        self.last_uuid = None

    def start(self, start_time=None):
        """
        Start a new API request with global lock to ensure thread/process safety.

        Args:
            start_time (datetime, optional): Specific start time. Defaults to current time.

        Returns:
            str: Unique identifier for the request
        """
        with APILimiter._global_lock:
            if start_time is None:
                start_time = datetime.now()
            self.last_uuid = str(uuid.uuid4())
            self.list.start(self.last_uuid, start_time)
            return self.last_uuid

    def done(self, uid=None, end_time=None):
        """
        Complete an API request with global lock to ensure thread/process safety.

        Args:
            uid (str, optional): Unique identifier. Defaults to last started request.
            end_time (datetime, optional): Specific end time. Defaults to current time.
        """
        with APILimiter._global_lock:
            if uid is None:
                uid = self.last_uuid
                if uid is None:
                    raise Exception("Not started.")
            
            if end_time is None:
                end_time = datetime.now()
            
            self.list.done(uid, end_time)
            self.last_uuid = None

    def check_wait(self, time=None):
        """
        Check waiting time with global lock to ensure thread/process safety.

        Args:
            time (datetime, optional): Time to check against. Defaults to current time.

        Returns:
            float: Waiting time in seconds, or 0 if no wait is needed
        """
        with APILimiter._global_lock:
            end_time = self.list.get_time(self.rpm)
            if end_time:
                if time is None:
                    time = datetime.now()
                t = (time - end_time).total_seconds()
                if t <= interval:
                    return math.ceil((interval - t) * 10) / 10
            return 0

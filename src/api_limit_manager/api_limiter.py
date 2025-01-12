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

            # Check waiting time and wait if necessary
            reference_time = self.list.get_time(self.rpm)
            if reference_time:
                t = (start_time - reference_time).total_seconds()
                if t <= interval:
                    return None, math.ceil((interval - t) * 10) / 10

            uid = str(uuid.uuid4())
            self.list.start(uid, start_time)
            return uid, None

    def done(self, uid, end_time=None):
        """
        Complete an API request with global lock to ensure thread/process safety.

        Args:
            uid (str): Unique identifier.
            end_time (datetime, optional): Specific end time. Defaults to current time.

        Raises:
            Exception: If the UID is invalid.
        """
        with APILimiter._global_lock:
            self.list.done(uid, end_time or datetime.now())

import math, uuid, platformdirs
from datetime import datetime
from multiprocessing import Lock
from .backend_list import BackendList
from .backend_sqlite import BackendSQLite

interval = 60 + 1  # with margin

def get_data_path():
    appname = __package__.split('.')[0]
    return platformdirs.user_data_path(appname, False, ensure_exists=True)

def get_data_file(file_name):
    return str(get_data_path() / file_name)

class APILimiter:
    _global_lock = Lock()

    def __init__(self, rpm = None, file_path=None):
        backend = BackendSQLite if file_path and str(file_path).endswith(".db") else BackendList
        self.list = backend(file_path)
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
        if uid is None:
            raise Exception("UID must be provided.")
        with APILimiter._global_lock:
            self.list.done(uid, end_time or datetime.now())

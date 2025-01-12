import os
from datetime import datetime, timedelta

class BackendList:
    def __init__(self, file_path=None):
        """
        Initialize BackendList with optional file-based persistence

        Args:
            file_path (str, optional): Path to the file or in-memory file
        """
        self.file_path = None if file_path == ':memory:' else file_path
        self.cache = ""
        self.entries = []
        self._load_entries()

    def _load_entries(self):
        """
        Load entries from a file-like object
        """
        if not self.file_path or not os.path.exists(self.file_path):
            return
        with open(self.file_path, "r") as f:
            self.cache = f.read()
        self.entries = []
        for line in self.cache.splitlines():
            parts = line.strip().split("\t")
            if len(parts) == 3:
                uid, start_time_str, end_time_str = parts
                start_time = datetime.fromisoformat(start_time_str)
                end_time = datetime.fromisoformat(end_time_str) if end_time_str else None
                self.entries.append((uid, start_time, end_time))

    def _save_entries(self, time=None):
        """
        Save entries to the file, removing entries older than 5 minutes
        """
        if time:
            cutoff_time = time - timedelta(minutes=5)
            self.entries = [entry for entry in self.entries if entry[2] >= cutoff_time]
        self.entries.sort(key=lambda x: x[2])
        self.cache = "\n".join(
            "\t".join((uid, start_time.isoformat(), end_time.isoformat()))
            for uid, start_time, end_time in self.entries
        )
        if self.file_path:
            with open(self.file_path, "w") as f:
                f.write(self.cache)

    def start(self, uid, start_time):
        """
        Start a new entry

        Args:
            uid (str): Unique identifier for the entry
            start_time (datetime): Start time of the entry
        """
        self._load_entries()
        end_time = start_time + timedelta(minutes=5)
        self.entries.append((uid, start_time, end_time))
        self._save_entries()

    def done(self, uid, end_time):
        """
        Complete an entry

        Args:
            uid (str): Unique identifier for the entry
            end_time (datetime): End time of the entry
        """
        self._load_entries()
        found = False
        for i, (entry_uid, start_time, _) in enumerate(self.entries):
            if entry_uid == uid:
                self.entries[i] = (uid, start_time, end_time)
                found = True
                break
        if not found:
            raise Exception(f"Not found: {uid}")
        self._save_entries(end_time)

    def get_time(self, index):
        """
        Get the end time of the last n entries

        Args:
            index (int): Number of entries to look back

        Returns:
            datetime or None: End time of the specified entry
        """
        if index is None:
            return None
        self._load_entries()
        if index > len(self.entries):
            return None
        return self.entries[-index][2]

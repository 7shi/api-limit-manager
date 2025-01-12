import sqlite3
from datetime import datetime, timedelta

class BackendSQLite:
    def __init__(self, db_path=":memory:"):
        """
        Initialize SQLite backend.

        Args:
            db_path (str): Path to the SQLite database file
        """
        self.conn = sqlite3.connect(
            db_path,
            check_same_thread=False
        )
        self.conn.execute('PRAGMA journal_mode=WAL')  # Write-Ahead Logging for better concurrency
        self.conn.execute('PRAGMA synchronous=NORMAL')  # Balance between performance and durability

        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_limit_entries (
                uid TEXT PRIMARY KEY,
                start_time DATETIME,
                end_time DATETIME
            )
        ''')

        # Add indexes
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_uid ON api_limit_entries(uid)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_end_time ON api_limit_entries(end_time)
        ''')

        self.conn.commit()

    def __del__(self):
        """
        Ensure connection is properly closed.
        """
        if self.conn:
            self.conn.close()
            self.conn = None

    def start(self, uid, start_time):
        """
        Start a new entry.

        Args:
            uid (str): Unique identifier for the entry
            start_time (datetime): Start time of the entry
        """
        end_time = start_time + timedelta(minutes=5)
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO api_limit_entries (uid, start_time, end_time)
            VALUES (?, ?, ?)
        ''', (uid, start_time, end_time))
        self.conn.commit()

    def done(self, uid, end_time):
        """
        Complete an entry and update its end time.

        Args:
            uid (str): Unique identifier for the entry
            end_time (datetime): End time of the entry

        Raises:
            Exception: If no entry is found for the given UID
        """
        cursor = self.conn.cursor()

        # Update the entry
        cursor.execute('''
            UPDATE api_limit_entries
            SET end_time = ?
            WHERE uid = ?
        ''', (end_time, uid))

        if cursor.rowcount == 0:
            raise Exception(f"Not found: {uid}")

        # Remove old entries (entries older than 5 minutes)
        cutoff_time = end_time - timedelta(minutes=5)
        cursor.execute('''
            DELETE FROM api_limit_entries
            WHERE start_time < ?
        ''', (cutoff_time,))

        self.conn.commit()

    def get_time(self, index):
        """
        Get the end time of an entry at the specified index.

        Args:
            index (int): Index of the entry to retrieve

        Returns:
            datetime or None: End time of the entry, or None if no entry exists
        """
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT end_time FROM api_limit_entries
            ORDER BY end_time DESC
            LIMIT 1 OFFSET ?
        ''', (index - 1,))
        result = cursor.fetchone()

        return datetime.fromisoformat(result[0]) if result else None

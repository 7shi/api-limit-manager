import os
import tempfile
from datetime import datetime, timedelta
import pytest
from api_limit_manager.backend_sqlite import BackendSQLite

@pytest.fixture
def backend_sqlite():
    """
    Test fixture using an in-memory SQLite database.
    """
    yield BackendSQLite()

def test_start_and_done_out_of_order(backend_sqlite):
    """
    Verify start and done operations in different orders.
    """
    base_time = datetime(2025, 1, 1, 0, 0, 0)

    # Start 3 items
    backend_sqlite.start('uid1', base_time)
    backend_sqlite.start('uid2', base_time + timedelta(seconds=1))
    backend_sqlite.start('uid3', base_time + timedelta(seconds=2))

    # Call done in a different order
    backend_sqlite.done('uid3', base_time + timedelta(seconds=5))
    backend_sqlite.done('uid1', base_time + timedelta(seconds=7))
    backend_sqlite.done('uid2', base_time + timedelta(seconds=10))

    # Verify get_time method behavior
    assert backend_sqlite.get_time(1) == base_time + timedelta(seconds=10)
    assert backend_sqlite.get_time(2) == base_time + timedelta(seconds=7)
    assert backend_sqlite.get_time(3) == base_time + timedelta(seconds=5)
    assert backend_sqlite.get_time(4) is None

def test_error_handling(backend_sqlite):
    """
    Verify error handling when calling done with a non-existent UID.
    """
    base_time = datetime(2025, 1, 12, 10, 0, 0)

    backend_sqlite.start('uid1', base_time)

    with pytest.raises(Exception) as excinfo:
        backend_sqlite.done('uid2', base_time + timedelta(seconds=5))

    assert 'Not found: uid2' in str(excinfo.value)

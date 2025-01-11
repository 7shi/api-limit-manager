from datetime import datetime, timedelta
import pytest
from api_limit_manager.backend_list import BackendList

def test_start_and_done_out_of_order():
    """
    Verify that the list is correctly sorted when multiple items are started
    and ended in a different order.
    """
    backend_list = BackendList()
    base_time = datetime(2025, 1, 1, 0, 0, 0)

    # Start 3 items (in different order)
    backend_list.start('uid1', base_time)
    backend_list.start('uid2', base_time + timedelta(seconds=1))
    backend_list.start('uid3', base_time + timedelta(seconds=2))

    # Call done in a different order
    backend_list.done('uid3', base_time + timedelta(seconds=5))
    backend_list.done('uid1', base_time + timedelta(seconds=7))
    backend_list.done('uid2', base_time + timedelta(seconds=10))

    # Check the list contents
    assert len(backend_list.list) == 3

    # Verify the list is correctly sorted
    assert backend_list.list[0][0] == 'uid3'
    assert backend_list.list[1][0] == 'uid1'
    assert backend_list.list[2][0] == 'uid2'

    # Verify end times are correct
    assert backend_list.list[0][2] == base_time + timedelta(seconds=5)
    assert backend_list.list[1][2] == base_time + timedelta(seconds=7)
    assert backend_list.list[2][2] == base_time + timedelta(seconds=10)

def test_get_time():
    """
    Verify the behavior of the get_time method.
    """
    backend_list = BackendList()
    base_time = datetime(2025, 1, 1, 0, 0, 0)

    backend_list.start('uid1', base_time)
    backend_list.start('uid2', base_time + timedelta(seconds=1))
    backend_list.start('uid3', base_time + timedelta(seconds=2))

    backend_list.done('uid1', base_time + timedelta(seconds=5))
    backend_list.done('uid2', base_time + timedelta(seconds=7))
    backend_list.done('uid3', base_time + timedelta(seconds=10))

    # Verify get_time method behavior
    assert backend_list.get_time(1) == base_time + timedelta(seconds=10)
    assert backend_list.get_time(2) == base_time + timedelta(seconds=7)
    assert backend_list.get_time(3) == base_time + timedelta(seconds=5)
    assert backend_list.get_time(4) is None

def test_error_handling():
    """
    Verify error handling when calling done with a non-existent UID.
    """
    backend_list = BackendList()
    base_time = datetime(2025, 1, 12, 10, 0, 0)

    backend_list.start('uid1', base_time)

    with pytest.raises(Exception) as excinfo:
        backend_list.done('uid2', base_time + timedelta(seconds=5))

    assert 'Not found: uid2' in str(excinfo.value)

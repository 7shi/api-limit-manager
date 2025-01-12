import pytest, os, tempfile, uuid
from datetime import datetime, timedelta
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
    assert len(backend_list.entries) == 3

    # Verify the list is correctly sorted
    assert backend_list.entries[0][0] == 'uid3'
    assert backend_list.entries[1][0] == 'uid1'
    assert backend_list.entries[2][0] == 'uid2'

    # Verify end times are correct
    assert backend_list.entries[0][2] == base_time + timedelta(seconds=5)
    assert backend_list.entries[1][2] == base_time + timedelta(seconds=7)
    assert backend_list.entries[2][2] == base_time + timedelta(seconds=10)

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

def test_backend_list_file_persistence():
    # Create a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
        temp_file_path = temp_file.name

    try:
        # Initialize BackendList with the file path
        backend_list = BackendList(file_path=temp_file_path)

        # Add an entry
        uid1 = str(uuid.uuid4())
        start_time1 = datetime.now()
        backend_list.start(uid1, start_time1)
        backend_list.done(uid1, start_time1 + timedelta(minutes=1))

        # Recreate the instance to verify persistence
        backend_list_reloaded = BackendList(file_path=temp_file_path)
        assert len(backend_list_reloaded.entries) == 1
        assert backend_list_reloaded.entries[0][0] == uid1
        assert backend_list_reloaded.entries[0][1] == start_time1
        assert backend_list_reloaded.entries[0][2] == start_time1 + timedelta(minutes=1)

    finally:
        # Remove the temporary file
        os.unlink(temp_file_path)

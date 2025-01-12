from datetime import datetime, timedelta
from api_limit_manager import APILimiter
import uuid

def test_start():
    # Initialize APILimiter
    limiter = APILimiter()

    # Test start method returns a valid UUID and no wait time
    request_id, wait_time = limiter.start()
    assert isinstance(request_id, str), "start method should return a string"
    assert wait_time is None, "wait time should be None for first request"

    # Validate UUID format
    try:
        uuid.UUID(request_id)
    except ValueError:
        assert False, "start method should return a valid UUID string"

    # Test done method with the generated request_id
    limiter.done(request_id)

    # Test start method returns a valid UUID and no wait time
    assert True, "Test passed"

def test_start_with_rpm_3_1():
    # Fix the current time
    base_time = datetime(2025, 1, 1, 0, 0, 0)

    # Initialize APILimiter (rpm=3)
    limiter = APILimiter(rpm=3)

    # Call start and done 2 times (1 second interval)
    for i in range(2):
        t = base_time + timedelta(seconds=i)
        request_id, _ = limiter.start(start_time=t)
        limiter.done(request_id, end_time=t)

    # 3rd check (verify if check_wait returns 0)
    _, result = limiter.start(base_time + timedelta(seconds=i+1))
    expected = None
    assert result == expected, f"Expected wait time to be {expected}, but got {result}"

def test_start_with_rpm_3_2():
    # Fix the current time
    base_time = datetime(2025, 1, 1, 0, 0, 0)

    # Initialize APILimiter (rpm=3)
    limiter = APILimiter(rpm=3)

    # Call start and done 3 times (1 second interval)
    for i in range(3):
        t = base_time + timedelta(seconds=i)
        request_id, _ = limiter.start(start_time=t)
        limiter.done(request_id, end_time=t)

    # 4th check (verify if check_wait returns 58)
    _, result = limiter.start(base_time + timedelta(seconds=i+1))
    expected = 58
    assert result == expected, f"Expected wait time to be {expected}, but got {result}"

def test_done_exception():
    # Initialize APILimiter
    limiter = APILimiter()

    # Test done method without uid raises an exception
    try:
        limiter.done(None)
        assert False, "done method should raise an exception when no UID is provided"
    except Exception as e:
        assert str(e) == "UID must be provided.", "Unexpected exception message"

from datetime import datetime, timedelta
from api_limit_manager import APILimiter
import uuid

def test_start():
    # Initialize APILimiter
    limiter = APILimiter()

    # Test start method returns a valid UUID and no wait time
    uid, wait_time = limiter.start()
    assert isinstance(uid, str), "start method should return a string"
    assert wait_time is None, "wait time should be None for first request"
    
    # Validate UUID format
    try:
        uuid.UUID(uid)
    except ValueError:
        assert False, "start method should return a valid UUID string"

    # Test done method with the generated UUID
    limiter.done()
    
    # Test that last_uuid is reset after done
    assert limiter.last_uuid is None, "last_uuid should be reset after done method"

def test_start_with_rpm_3_1():
    # Fix the current time
    base_time = datetime(2025, 1, 1, 0, 0, 0)

    # Initialize APILimiter (rpm=3)
    limiter = APILimiter(rpm=3)

    # Call start and done 2 times (1 second interval)
    for i in range(2):
        t = base_time + timedelta(seconds=i)
        limiter.start(start_time=t)
        limiter.done(end_time=t)

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
        limiter.start(start_time=t)
        limiter.done(end_time=t)

    # 4th check (verify if check_wait returns 58)
    _, result = limiter.start(base_time + timedelta(seconds=i+1))
    expected = 58
    assert result == expected, f"Expected wait time to be {expected}, but got {result}"

def test_done_exception():
    # Initialize APILimiter
    limiter = APILimiter()

    # Test done method without start raises an exception
    try:
        limiter.done()
        assert False, "done method should raise an exception when not started"
    except Exception as e:
        assert str(e) == "Not started.", "Unexpected exception message"

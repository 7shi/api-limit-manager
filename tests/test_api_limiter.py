from datetime import datetime, timedelta
from api_limit_manager import APILimiter
import uuid

def test_start_method():
    # Initialize APILimiter
    limiter = APILimiter()

    # Test start method returns a valid UUID
    uid = limiter.start()
    assert isinstance(uid, str), "start method should return a string"
    
    # Validate UUID format
    try:
        uuid.UUID(uid)
    except ValueError:
        assert False, "start method should return a valid UUID string"

    # Test done method with the generated UUID
    limiter.done()
    
    # Test that last_uuid is reset after done
    assert limiter.last_uuid is None, "last_uuid should be reset after done method"

def test_start_method_exception():
    # Initialize APILimiter
    limiter = APILimiter()

    # Test done method without start raises an exception
    try:
        limiter.done()
        assert False, "done method should raise an exception when not started"
    except Exception as e:
        assert str(e) == "Not started.", "Unexpected exception message"

def test_check_wait_with_rpm_3_1():
    # Fix the current time
    base_time = datetime(2025, 1, 1, 0, 0, 0)

    # Initialize APILimiter (rpm=3)
    limiter = APILimiter(rpm=3)

    # Call start and done 2 times (1 second interval)
    for i in range(2):
        limiter.start()
        limiter.done(end_time=base_time + timedelta(seconds=i))

    # 3rd check (verify if check_wait returns 0)
    result = limiter.check_wait(base_time + timedelta(seconds=2))
    expected = 0
    assert result == expected, f"Expected wait time to be {expected}, but got {result}"

def test_check_wait_with_rpm_3_2():
    # Fix the current time
    base_time = datetime(2025, 1, 1, 0, 0, 0)

    # Initialize APILimiter (rpm=3)
    limiter = APILimiter(rpm=3)

    # Call start and done 3 times (1 second interval)
    for i in range(3):
        limiter.start()
        limiter.done(end_time=base_time + timedelta(seconds=i))

    # 4th check (verify if check_wait returns 58)
    result = limiter.check_wait(base_time + timedelta(seconds=3))
    expected = 58
    assert result == expected, f"Expected wait time to be {expected}, but got {result}"

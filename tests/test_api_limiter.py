from datetime import datetime, timedelta
from api_limit_manager import APILimiter

def test_check_wait_with_rpm_3_1():
    # Fix the current time
    base_time = datetime(2025, 1, 1, 0, 0, 0)

    # Initialize APILimiter (rpm=3)
    limiter = APILimiter(rpm=3)

    # Call done 2 times (1 second interval)
    for i in range(2):
        limiter.done(base_time + timedelta(seconds=i))

    # 3rd check (verify if check_wait returns 0)
    result = limiter.check_wait(base_time + timedelta(seconds=2))
    expected = 0
    assert result == expected, f"Expected wait time to be {expected}, but got {result}"

def test_check_wait_with_rpm_3_2():
    # Fix the current time
    base_time = datetime(2025, 1, 1, 0, 0, 0)

    # Initialize APILimiter (rpm=3)
    limiter = APILimiter(rpm=3)

    # Call done 3 times (1 second interval)
    for i in range(3):
        limiter.done(base_time + timedelta(seconds=i))

    # 4th check (verify if check_wait returns 61)
    result = limiter.check_wait(base_time + timedelta(seconds=3))
    expected = 58
    assert result == expected, f"Expected wait time to be {expected}, but got {result}"

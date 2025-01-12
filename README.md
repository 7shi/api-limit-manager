# API Limit Manager

## Overview

`api-limit-manager` is a Python library designed to help developers manage API request rates and prevent rate limiting errors. It provides a simple and flexible way to control the number of requests made to an API within a specified time interval.

## Features

- Configurable request rate limits
- Easy-to-use API limiter class
- Automatic waiting time calculation
- Supports dynamic rate limit management

## Requirements

- Python 3.10+
- No external dependencies required

## Usage

```python
from api_limit_manager import APILimiter

# Create an APILimiter with a rate limit of 60 requests per minute
limiter = APILimiter(rpm=10)

# Start a new API request
# Retry until a request can be made
request_id = None
for _ in range(3):
    request_id, wait_time = limiter.start()
    if request_id:
        break
    time.sleep(wait_time)
if request_id is None:
    raise Exception("Could not acquire API request after 3 attempts.")

# Make your API call
response = make_api_request()

# Mark the request as completed
limiter.done(request_id)
```

## Backends

The API Limit Manager supports two types of backends for persistence:

- `BackendList`: a simple text file-based backend
- `BackendSQLite`: an alternative backend using SQLite.

The backend is selected based on the file extension. If the file has a `.db` extension, the `BackendSQLite` is used; otherwise, the `BackendList` is used.

### Backend Selection Example

```python
from api_limit_manager import APILimiter, get_data_file

# Use default text file backend (without creating an actual file)
limiter = APILimiter()

# Use a auto-generated text file
limiter = APILimiter(file_path=get_data_file("my_api.txt"))

# Use a auto-generated SQLite file
limiter = APILimiter(file_path=get_data_file("my_api.db"))
```

# utils/error_handler.py
import redis

def handle_redis_errors(func):
    """
    Decorator to handle Redis connection errors for Redis operations.

    Args:
        func (function): Function to wrap with error handling.

    Returns:
        function: Wrapped function with error handling.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except redis.ConnectionError as e:
            print(f"Redis connection error: {e}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    return wrapper

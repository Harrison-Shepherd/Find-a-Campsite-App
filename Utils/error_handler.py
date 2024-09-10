import redis

def handle_redis_errors(func):
    """
    Decorator to handle Redis connection errors and other general exceptions
    during Redis operations.

    Args:
        func (function): The function to wrap with error handling.

    Returns:
        function: The wrapped function with error handling that catches Redis connection errors
                  and other general exceptions, providing a safe fallback.
    """
    def wrapper(*args, **kwargs):
        try:
            # Execute the wrapped function
            return func(*args, **kwargs)
        except redis.ConnectionError as e:
            # Handle Redis-specific connection errors
            print(f"Redis connection error: {e}")
            return None
        except Exception as e:
            # Handle any other general exceptions
            print(f"An error occurred: {e}")
            return None

    return wrapper

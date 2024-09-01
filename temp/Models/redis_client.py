import redis
from Utils.error_handler import handle_redis_errors

class RedisClient:
    def __init__(self, host, port, password, ssl=False):
        """
        Initializes the Redis client with the given parameters.

        Args:
            host (str): The Redis server host.
            port (int): The Redis server port.
            password (str): The password for authenticating with Redis.
            ssl (bool): Whether to use SSL for the connection.
        """
        try:
            # Create a Redis client connection
            self.client = redis.Redis(
                host=host,
                port=port,
                password=password,
                ssl=ssl,
                decode_responses=True  # Automatically decode responses to string
            )
            # Test the connection
            self.client.ping()
            print("Connected to Redis successfully.")
        except redis.ConnectionError as e:
            print(f"Failed to connect to Redis: {e}")
            self.client = None

    @handle_redis_errors
    def exists(self, key):
        return self.client.exists(key) > 0

    @handle_redis_errors
    def hgetall(self, key):
        return self.client.hgetall(key)

    @handle_redis_errors
    def hget(self, key, field):
        return self.client.hget(key, field)

    @handle_redis_errors
    def hset(self, key, mapping):
        return self.client.hset(key, mapping=mapping)

    @handle_redis_errors
    def delete(self, key):
        return self.client.delete(key)

    def keys(self, pattern="*"):
        """
        Lists all keys matching a pattern.

        Args:
            pattern (str): The pattern to match keys.

        Returns:
            list: List of matching keys.
        """
        try:
            return self.client.keys(pattern) if self.client else []
        except redis.ConnectionError as e:
            print(f"Error listing keys: {e}")
            return []

import redis
from Utils.error_handler import handle_redis_errors

class RedisClient:
    """
    A class for managing Redis client operations with connection handling and error management.
    """

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
                decode_responses=True  # Automatically decode responses to strings
            )
            # Test the connection
            self.client.ping()
            print("Connected to Redis successfully.")
        except redis.ConnectionError as e:
            print(f"Failed to connect to Redis: {e}")
            self.client = None

    @handle_redis_errors
    def exists(self, key):
        """
        Checks if a key exists in the Redis database.

        Args:
            key (str): The key to check.

        Returns:
            bool: True if the key exists, False otherwise.
        """
        return self.client.exists(key) > 0

    @handle_redis_errors
    def hgetall(self, key):
        """
        Retrieves all fields and values of a hash stored at key.

        Args:
            key (str): The key of the hash.

        Returns:
            dict: A dictionary of fields and values in the hash.
        """
        return self.client.hgetall(key)

    @handle_redis_errors
    def hget(self, key, field):
        """
        Retrieves the value associated with the field in the hash stored at key.

        Args:
            key (str): The key of the hash.
            field (str): The field in the hash.

        Returns:
            str: The value associated with the field.
        """
        return self.client.hget(key, field)

    @handle_redis_errors
    def hset(self, key, mapping):
        """
        Sets the specified fields to their respective values in the hash stored at key.

        Args:
            key (str): The key of the hash.
            mapping (dict): A dictionary of field-value pairs to set.

        Returns:
            int: The number of fields that were added to the hash.
        """
        return self.client.hset(key, mapping=mapping)

    @handle_redis_errors
    def delete(self, key):
        """
        Deletes the specified key from the Redis database.

        Args:
            key (str): The key to delete.

        Returns:
            int: The number of keys that were removed.
        """
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

import redis

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

    def exists(self, key):
        """
        Checks if a key exists in Redis.

        Args:
            key (str): The key to check.

        Returns:
            bool: True if the key exists, False otherwise.
        """
        try:
            return self.client.exists(key) > 0 if self.client else False
        except redis.ConnectionError as e:
            print(f"Error checking key existence: {e}")
            return False

    def hgetall(self, key):
        """
        Retrieves all fields and values of a hash stored at key.

        Args:
            key (str): The key of the hash.

        Returns:
            dict: A dictionary of fields and values.
        """
        try:
            return self.client.hgetall(key) if self.client else {}
        except redis.ConnectionError as e:
            print(f"Error retrieving data: {e}")
            return {}

    def hget(self, key, field):
        """
        Retrieves the value of a specific field from a hash stored at key.

        Args:
            key (str): The key of the hash.
            field (str): The field to retrieve.

        Returns:
            str: The value of the field, or None if the field does not exist.
        """
        try:
            return self.client.hget(key, field) if self.client else None
        except redis.ConnectionError as e:
            print(f"Error retrieving field data: {e}")
            return None

    def hset(self, key, mapping):
        """
        Sets multiple fields in a hash.

        Args:
            key (str): The key of the hash.
            mapping (dict): The fields and values to set.

        Returns:
            int: The number of fields that were added.
        """
        try:
            return self.client.hset(key, mapping=mapping) if self.client else 0
        except redis.ConnectionError as e:
            print(f"Error setting data: {e}")
            return 0

    def delete(self, key):
        """
        Deletes a key from Redis.

        Args:
            key (str): The key to delete.

        Returns:
            int: The number of keys that were removed.
        """
        try:
            return self.client.delete(key) if self.client else 0
        except redis.ConnectionError as e:
            print(f"Error deleting key: {e}")
            return 0

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

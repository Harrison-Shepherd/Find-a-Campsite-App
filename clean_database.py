from Models.redis_client import RedisClient

def clean_redis_database():
    """
    Cleans the Redis database by deleting all keys.
    """
    try:
        # Initialize the Redis client with connection parameters
        redis_client = RedisClient(
            host='mycampsiteredis.redis.cache.windows.net',
            port=6380,
            password='F21P4lrm3B63A5nNWUldt528Usqtped65AzCaNnjtg8=',
            ssl=True
        ).client
        
        # Retrieve all keys in the Redis database
        keys = redis_client.keys('*')
        if not keys:
            print("The Redis database is already clean.")
            return

        # Delete all keys from the database
        for key in keys:
            redis_client.delete(key)

        print("All data has been successfully cleared from the Redis database.")
    except Exception as e:
        print(f"Failed to clean the Redis database: {e}")

if __name__ == "__main__":
    clean_redis_database()

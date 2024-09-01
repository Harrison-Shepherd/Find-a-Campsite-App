import bcrypt
import unittest
from Models.account import Account
from Models.redis_client import RedisClient

class TestAccountLogin(unittest.TestCase):

    def setUp(self):
        """Set up Redis client and create Account instance for testing."""
        self.redis_client = RedisClient(
            host="mycampsiteredis.redis.cache.windows.net",
            port=6380,
            password="F21P4lrm3B63A5nNWUldt528Usqtped65AzCaNnjtg8=",
            ssl=True
        ).client
        self.account_manager = Account(self.redis_client)
        self.clear_redis_data()

        # Pre-hash the password to simulate how it's stored
        hashed_password = bcrypt.hashpw("testpw123".encode('utf-8'), bcrypt.gensalt())
        self.redis_client.hset("testuser@gmail.com", mapping={
            'password': hashed_password.decode('utf-8'),
            'first_name': 'Test',
            'security_answer': 'Molly'
        })

    def clear_redis_data(self):
        """Clear existing Redis data to prevent test interference."""
        for key in self.redis_client.keys('*'):
            self.redis_client.delete(key)

    def test_successful_login(self):
        """Test login with correct credentials."""
        result = self.account_manager.login("testuser@gmail.com", "testpw123")
        self.assertTrue(result, "Login should succeed with correct credentials.")

    def test_incorrect_password(self):
        """Test login with an incorrect password."""
        result = self.account_manager.login("testuser@gmail.com", "wrongpassword")
        self.assertFalse(result, "Login should fail with incorrect password.")

    def tearDown(self):
        """Clean up Redis data after each test."""
        self.clear_redis_data()

if __name__ == '__main__':
    unittest.main()

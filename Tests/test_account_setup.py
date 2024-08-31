# Tests/test_account_setup.py
import unittest
from unittest.mock import patch
import logging
from Models.account import Account
from Models.redis_client import RedisClient

# Configure logging
logging.basicConfig(level=logging.INFO)

class TestAccountSetup(unittest.TestCase):

    def setUp(self):
        """
        Set up the Redis client and Account manager before each test.
        Clear Redis data to ensure a clean start.
        """
        logging.info("Setting up Redis client and Account manager.")
        self.redis_client = RedisClient(
            host="mycampsiteredis.redis.cache.windows.net",
            port=6380,
            password="F21P4lrm3B63A5nNWUldt528Usqtped65AzCaNnjtg8=",
            ssl=True
        )
        self.account_manager = Account(self.redis_client)
        self.clear_redis_data()

    def clear_redis_data(self):
        """
        Clears all keys in Redis to avoid test conflicts.
        """
        logging.info("Clearing Redis data.")
        for key in self.redis_client.keys('*'):
            self.redis_client.delete(key)

    @patch('builtins.input', side_effect=["cat's name", 'Percy'])
    def test_account_creation(self, mock_input):
        """
        Test creating a new account with valid inputs.
        """
        self.account_manager.create_account(
            login_name="test@gmail.com",
            password="testpw123",
            first_name="Harrison"
        )
        stored_account = self.redis_client.hgetall("test@gmail.com")
        self.assertIn('first_name', stored_account)
        self.assertEqual(stored_account['first_name'], "Harrison")
        # Updated expected question to include the question mark
        self.assertEqual(stored_account['security_question'], "cat's name?")
        self.assertEqual(stored_account['security_answer'], "Percy")

    @patch('builtins.input', side_effect=["cat's name", 'Percy'])
    def test_successful_login(self, mock_input):
        """
        Test successful login with correct credentials.
        """
        self.account_manager.create_account(
            login_name="test@gmail.com",
            password="testpw123",
            first_name="Harrison"
        )
        result = self.account_manager.login("test@gmail.com", "testpw123")
        self.assertTrue(result)

    @patch('builtins.input', side_effect=["cat's name", 'Percy'])
    def test_invalid_password_login(self, mock_input):
        """
        Test login attempt with an incorrect password.
        """
        self.account_manager.create_account(
            login_name="test@gmail.com",
            password="testpw123",
            first_name="Harrison"
        )
        result = self.account_manager.login("test@gmail.com", "wrongpassword")
        self.assertFalse(result)

    def test_non_existent_account_login(self):
        """
        Test login attempt with a non-existent account.
        """
        result = self.account_manager.login("nonuser@example.com", "password")
        self.assertFalse(result)

    def tearDown(self):
        """
        Clean up after each test by removing test data from Redis.
        """
        logging.info("Tearing down: Clearing Redis data after test.")
        self.clear_redis_data()


if __name__ == '__main__':
    unittest.main()

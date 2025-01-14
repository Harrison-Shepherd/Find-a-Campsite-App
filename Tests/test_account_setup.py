import unittest
from unittest.mock import patch
import logging
from Models.account import Account
from Models.redis_client import RedisClient

# Configure logging to display INFO level messages
logging.basicConfig(level=logging.INFO)

class TestAccountSetup(unittest.TestCase):
    """
    Unit tests for setting up accounts using the Account class.
    """

    def setUp(self):
        """
        Set up the Redis client and Account manager before each test.
        Clears Redis data to ensure a clean state for testing.
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
        Clears all keys in Redis to avoid conflicts between tests.
        """
        logging.info("Clearing Redis data.")
        for key in self.redis_client.keys('*'):
            self.redis_client.delete(key)

    @patch('builtins.input', side_effect=["cat's name", 'Percy'])
    def test_account_creation(self, mock_input):
        """
        Test creating a new account with valid inputs.
        Verifies that the account details are correctly stored in Redis.
        """
        self.account_manager.create_account(
            login_name="test@gmail.com",
            password="testpw123",
            first_name="Harrison"
        )
        stored_account = self.redis_client.hgetall("test@gmail.com")
        self.assertIn('first_name', stored_account)
        self.assertEqual(stored_account['first_name'], "Harrison")
        self.assertEqual(stored_account['security_question'], "cat's name?")
        self.assertEqual(stored_account['security_answer'], "Percy")

    @patch('builtins.input', side_effect=["cat's name", 'Percy'])
    def test_create_account_with_invalid_email(self, mock_input):
        """
        Test account creation with an invalid email format.
        Ensures that account creation fails when the email format is invalid.
        """
        result = self.account_manager.create_account(
            login_name="invalidemail", 
            password="password123", 
            first_name="John"
        )
        self.assertIsNone(result, "Account creation should fail with an invalid email format.")

    @patch('builtins.input', side_effect=["cat's name", 'Percy'])
    def test_create_account_with_missing_fields(self, mock_input):
        """
        Test account creation with missing required fields.
        Ensures that account creation fails when required fields are not provided.
        """
        result = self.account_manager.create_account(
            login_name="missingfields@example.com", 
            password="",  # Missing password
            first_name=""
        )
        self.assertIsNone(result, "Account creation should fail when required fields are missing.")

    def tearDown(self):
        """
        Clean up after each test by removing test data from Redis.
        """
        logging.info("Tearing down: Clearing Redis data after test.")
        self.clear_redis_data()

if __name__ == '__main__':
    unittest.main()

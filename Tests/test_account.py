import unittest
from unittest.mock import patch
import logging
from Models.account import Account
from Models.redis_client import RedisClient

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class TestAccount(unittest.TestCase):

    def setUp(self):
        """
        Set up the Redis client and Account manager before each test.
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
            logging.debug(f"Deleting key: {key}")
            self.redis_client.delete(key)

    @patch('builtins.input', side_effect=['cat', 'cat'])
    def test_account_creation(self, mock_input):
        """
        Test creating a new account with valid inputs.
        """
        logging.info("Testing account creation.")
        self.account_manager.create_account(
            login_name="krety28@gmail.com",
            password="testing47",
            first_name="harrison"
        )
        stored_account = self.redis_client.hgetall("krety28@gmail.com")
        logging.debug(f"Stored account: {stored_account}")
        self.assertIn('first_name', stored_account)
        self.assertEqual(stored_account['first_name'], "harrison")

    @patch('builtins.input', side_effect=['cat', 'cat'])
    def test_successful_login(self, mock_input):
        """
        Test successful login with correct credentials.
        """
        self.account_manager.create_account(
            login_name="krety28@gmail.com",
            password="testing47",
            first_name="harrison"
        )
        result = self.account_manager.login("krety28@gmail.com", "testing47")
        logging.info(f"Login result: {result}")
        self.assertTrue(result)

    @patch('builtins.input', side_effect=['cat', 'cat'])
    def test_invalid_password_login(self, mock_input):
        """
        Test login attempt with an incorrect password.
        """
        logging.info("Testing login with incorrect password.")
        self.account_manager.create_account(
            login_name="krety28@gmail.com",
            password="testing47",
            first_name="harrison"
        )
        result = self.account_manager.login("krety28@gmail.com", "wrongpassword")
        logging.warning(f"Login result with wrong password: {result}")
        self.assertFalse(result)

    def test_non_existent_account_login(self):
        """
        Test login attempt with a non-existent account.
        """
        logging.info("Testing login with a non-existent account.")
        result = self.account_manager.login("nonuser@example.com", "password")
        logging.debug(f"Login result for non-existent account: {result}")
        self.assertFalse(result)

    @patch('builtins.input', side_effect=['correct_answer', 'newpassword'])
    def test_password_reset_with_correct_security_answer(self, mock_input):
        """
        Test password reset with the correct security question answer.
        """
        logging.info("Testing password reset with correct security answer.")
        self.account_manager.create_account(
            login_name="krety28@gmail.com",
            password="testing47",
            first_name="harrison"
        )

        # Set the expected security answer explicitly in Redis
        self.redis_client.hset("krety28@gmail.com", mapping={
            'security_question': 'test',
            'security_answer': 'correct_answer'
        })

        # Log the stored values for verification
        stored_security_answer = self.redis_client.hget("krety28@gmail.com", 'security_answer')
        logging.debug(f"Stored security answer: '{stored_security_answer}'")

        # Attempt to reset the password with correct security question answer
        result = self.account_manager.forgot_password("krety28@gmail.com")

        logging.debug(f"Password reset result with correct answer: {result}")

        # Verify that the account still exists
        stored_account = self.redis_client.hgetall("krety28@gmail.com")
        logging.debug(f"Stored account after password reset attempt: {stored_account}")

        # Extract and log the user-provided answer from the mocked input
        user_answer = mock_input.call_args_list[0][0][0]  # Extract the mocked user answer input
        logging.debug(f"User provided answer: '{user_answer}'")
        logging.debug(f"Comparing with stored answer: '{stored_security_answer}'")

        # Assertion to ensure the reset was successful
        self.assertTrue(result)

    @patch('builtins.input', side_effect=['test', 'wronganswer', 'dummy_input'])
    def test_password_reset_with_incorrect_security_answer(self, mock_input):
        """
        Test password reset with an incorrect security question answer.
        """
        logging.info("Testing password reset with incorrect security answer.")
        self.account_manager.create_account(
            login_name="krety28@gmail.com",
            password="testing47",
            first_name="harrison"
        )
        result = self.account_manager.forgot_password("krety28@gmail.com")
        logging.warning(f"Password reset result with incorrect answer: {result}")
        self.assertFalse(result)

    def tearDown(self):
        """
        Clean up after each test by removing test data from Redis.
        """
        logging.info("Tearing down: Clearing Redis data after test.")
        self.clear_redis_data()


if __name__ == '__main__':
    unittest.main()

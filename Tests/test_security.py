# Tests/test_security.py
from unittest.mock import patch
import unittest
import logging
import time
from Models.account import Account
from Models.redis_client import RedisClient

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def delayed_input(prompt_sequence):
    """
    Generator function to simulate delayed input responses for testing.
    This helps synchronize test inputs, especially when multiple prompts are expected.
    """
    for prompt in prompt_sequence:
        logging.debug(f"Providing input: {prompt}")
        time.sleep(0.7)  # Delay between each input to simulate user interaction
        yield prompt

class TestPasswordReset(unittest.TestCase):
    """
    Tests for password reset functionality, focusing on security questions and answers.
    """

    def setUp(self):
        """
        Set up the Redis client and Account manager before each test.
        Initializes a connection to Redis and ensures a clean environment.
        """
        logging.info("Setting up Redis client and Account manager.")
        self.redis_client = RedisClient(
            host="mycampsiteredis.redis.cache.windows.net",
            port=6380,
            password="F21P4lrm3B63A5nNWUldt528Usqtped65AzCaNnjtg8=",
            ssl=True
        )
        self.account_manager = Account(self.redis_client)
        self.clear_redis_data()  # Clear Redis data to avoid test conflicts

    def clear_redis_data(self):
        """
        Clears all keys in Redis to ensure each test starts with no data.
        """
        logging.info("Clearing Redis data.")
        for key in self.redis_client.keys('*'):
            logging.debug(f"Deleting key: {key}")
            self.redis_client.delete(key)

    @patch('builtins.input', side_effect=lambda prompt: delayed_input(['Percy', 'new_password_123', 'new_password_123']).__next__())
    def test_password_reset_with_correct_security_answer(self, mock_input):
        """
        Test password reset with the correct security question answer.
        Verifies that providing the correct answer allows a password reset.
        """
        logging.info("Testing password reset with correct security answer.")

        # Create a test account with the specified details
        self.account_manager.create_account(
            login_name="test@gmail.com",
            password="testpw123",
            first_name="Harrison"
        )

        # Set custom security question and answer directly in Redis
        self.redis_client.hset("test@gmail.com", mapping={
            "security_question": "cat's name",
            "security_answer": "Percy"
        })

        # Check stored security details in Redis for verification
        stored_security_question = self.redis_client.hget("test@gmail.com", 'security_question')
        stored_security_answer = self.redis_client.hget("test@gmail.com", 'security_answer')
        logging.debug(f"Stored security question: '{stored_security_question}'")
        logging.debug(f"Stored security answer: '{stored_security_answer}'")

        # Attempt to reset the password with the correct answer
        result = self.account_manager.forgot_password("test@gmail.com")

        # Check the result of the password reset attempt
        logging.debug(f"Password reset result: {result}")

        # Verify the account details after the reset attempt
        stored_account = self.redis_client.hgetall("test@gmail.com")
        logging.debug(f"Stored account after password reset attempt: {stored_account}")

        # Assert that the password reset was successful
        self.assertTrue(result)

    @patch('builtins.input', side_effect=lambda prompt: delayed_input(['wronganswer']).__next__())
    def test_password_reset_with_incorrect_security_answer(self, mock_input):
        """
        Test password reset with an incorrect security question answer.
        Ensures that an incorrect answer prevents the password reset.
        """
        logging.info("Testing password reset with incorrect security answer.")

        # Create a test account with a security question and answer
        self.account_manager.create_account(
            login_name="test@gmail.com",
            password="testpw123",
            first_name="Harrison"
        )

        # Set the custom security question and answer in Redis
        self.redis_client.hset("test@gmail.com", mapping={
            "security_question": "cat's name",
            "security_answer": "Percy"
        })

        # Attempt to reset the password with the incorrect answer
        result = self.account_manager.forgot_password("test@gmail.com")
        logging.warning(f"Password reset result with incorrect answer: {result}")

        # Assert that the password reset was unsuccessful
        self.assertFalse(result)

    def tearDown(self):
        """
        Clean up after each test by removing test data from Redis.
        Ensures no data remains to affect subsequent tests.
        """
        logging.info("Tearing down: Clearing Redis data after test.")
        self.clear_redis_data()

if __name__ == '__main__':
    unittest.main()

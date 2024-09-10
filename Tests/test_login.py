import bcrypt
import unittest
from Models.account import Account
from Models.redis_client import RedisClient

class TestAccountLogin(unittest.TestCase):
    """
    Unit tests for the Account login functionality.
    """

    def setUp(self):
        """
        Set up Redis client and create Account instance for testing.
        Initializes test data in Redis with a predefined account.
        """
        self.redis_client = RedisClient(
            host="mycampsiteredis.redis.cache.windows.net",
            port=6380,
            password="F21P4lrm3B63A5nNWUldt528Usqtped65AzCaNnjtg8=",
            ssl=True
        ).client
        self.account_manager = Account(self.redis_client)
        self.clear_redis_data()

        # Pre-hash the password to simulate stored credentials
        hashed_password = bcrypt.hashpw("testpw123".encode('utf-8'), bcrypt.gensalt())
        self.redis_client.hset("testuser@gmail.com", mapping={
            'password': hashed_password.decode('utf-8'),
            'first_name': 'Test',
            'security_answer': 'Molly'
        })

    def clear_redis_data(self):
        """
        Clear all existing Redis data to ensure tests do not interfere with each other.
        """
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

    def test_password_with_trailing_spaces(self):
        """Test login with a correct password but with trailing spaces."""
        result = self.account_manager.login("testuser@gmail.com", "testpw123 ")
        self.assertFalse(result, "Login should fail if the password has trailing spaces.")

    def test_password_with_leading_spaces(self):
        """Test login with a correct password but with leading spaces."""
        result = self.account_manager.login("testuser@gmail.com", " testpw123")
        self.assertFalse(result, "Login should fail if the password has leading spaces.")

    def test_password_case_sensitivity(self):
        """Test login with a correct password but with altered case."""
        result = self.account_manager.login("testuser@gmail.com", "TestPW123")
        self.assertFalse(result, "Login should fail if the password case does not match.")

    def test_empty_password(self):
        """Test login with an empty password."""
        result = self.account_manager.login("testuser@gmail.com", "")
        self.assertFalse(result, "Login should fail if the password is empty.")

    def test_empty_username(self):
        """Test login with an empty username."""
        result = self.account_manager.login("", "testpw123")
        self.assertFalse(result, "Login should fail if the username is empty.")

    def test_login_nonexistent_account(self):
        """Test login attempt on a nonexistent account."""
        result = self.account_manager.login("nonexistent@gmail.com", "testpw123")
        self.assertFalse(result, "Login should fail for a nonexistent account.")

    def tearDown(self):
        """
        Clean up Redis data after each test to ensure a fresh start for the next test.
        """
        self.clear_redis_data()

if __name__ == '__main__':
    unittest.main()

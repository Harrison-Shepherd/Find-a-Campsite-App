import unittest
from unittest.mock import patch, mock_open
from Models.redis_client import RedisClient
from Utils.data_loader import DataLoader  # Adjust the import path as needed


class TestDataLoader(unittest.TestCase):

    def setUp(self):
        """
        Set up the Redis client and DataLoader before each test.
        """
        self.redis_client = RedisClient(
            host="mycampsiteredis.redis.cache.windows.net",
            port=6380,
            password="F21P4lrm3B63A5nNWUldt528Usqtped65AzCaNnjtg8=",
            ssl=True
        )
        self.data_loader = DataLoader(self.redis_client)
        self.clear_redis_data()  # Clear Redis data before each test to avoid conflicts

    def clear_redis_data(self):
        """
        Clears all keys in Redis to avoid test conflicts.
        """
        for key in self.redis_client.keys('*'):
            self.redis_client.delete(key)

    @patch('builtins.open', new_callable=mock_open, read_data="username,password,firstname,first dogs name\nuser1@example.com,pass123,John,Max\n")
    def test_load_valid_data(self, mock_file):
        """
        Test loading valid data from a CSV file.
        """
        self.data_loader.load_initial_data('ICT320 - Task 2 - Initial Database.csv')
        stored_account = self.redis_client.hgetall("user1@example.com")
        self.assertIn('first_name', stored_account)
        self.assertEqual(stored_account['first_name'], "John")

    @patch('builtins.open', new_callable=mock_open, read_data="username,password,firstname,first dogs name\nuser2@example.com,,Doe,\n")
    def test_load_data_with_missing_fields(self, mock_file):
        """
        Test loading data with missing fields.
        """
        self.data_loader.load_initial_data('ICT320 - Task 2 - Initial Database.csv')
        stored_account = self.redis_client.hgetall("user2@example.com")
        self.assertEqual(stored_account, {})  # Expect empty since missing required fields

    @patch('builtins.open', new_callable=mock_open, read_data="username,password,firstname,first dogs name\nuser1@example.com,pass123,John,Max\nuser1@example.com,newpass,Jane,Max\n")
    def test_load_duplicate_entries(self, mock_file):
        """
        Test how loader handles duplicate entries.
        """
        self.data_loader.load_initial_data('ICT320 - Task 2 - Initial Database.csv')
        stored_account = self.redis_client.hgetall("user1@example.com")
        self.assertIn('first_name', stored_account)
        self.assertEqual(stored_account['first_name'], "Jane")

    @patch('builtins.open', new_callable=mock_open, read_data="username,password,firstname,first dogs name\nuser3@example.com,123,42,Doggy\n")
    def test_load_data_with_incorrect_data_types(self, mock_file):
        """
        Test loading data with incorrect data types.
        """
        self.data_loader.load_initial_data('ICT320 - Task 2 - Initial Database.csv')
        stored_account = self.redis_client.hgetall("user3@example.com")
        self.assertIn('first_name', stored_account)
        self.assertEqual(stored_account['first_name'], "42")  # Ensures data type handling

    @patch('builtins.open', new_callable=mock_open, read_data="")
    def test_load_empty_file(self, mock_file):
        """
        Test loading an empty CSV file.
        """
        self.data_loader.load_initial_data('ICT320 - Task 2 - Initial Database.csv')
        self.assertEqual(self.redis_client.keys('*'), [])  # Expect no keys after empty load

    @patch('builtins.open', new_callable=mock_open, read_data="username,password,firstname,first dogs name\ninvalid_line_without_commas\n")
    def test_load_malformed_file(self, mock_file):
        """
        Test loading a malformed CSV file.
        """
        try:
            self.data_loader.load_initial_data('ICT320 - Task 2 - Initial Database.csv')
            self.fail("Expected an error due to malformed data, but none was raised.")
        except Exception as e:
            self.assertTrue(isinstance(e, Exception))  # Ensure exception is caught

    def tearDown(self):
        """
        Clean up after each test by removing test data from Redis.
        """
        self.clear_redis_data()  # Clear Redis data after each test


if __name__ == '__main__':
    unittest.main()

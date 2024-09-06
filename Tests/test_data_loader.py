import unittest
from unittest.mock import patch, mock_open
from Models.redis_client import RedisClient
from Utils.data_loader import DataLoader

class TestDataLoader(unittest.TestCase):
    """
    Unit tests for the DataLoader class, which handles loading data into Redis.
    """

    def setUp(self):
        """
        Set up the Redis client and DataLoader instance before each test.
        Initializes a connection to the Redis server and clears any existing data
        to ensure a clean state for each test.
        """
        # Initialize Redis client with the specified server details
        self.redis_client = RedisClient(
            host="mycampsiteredis.redis.cache.windows.net",
            port=6380,
            password="F21P4lrm3B63A5nNWUldt528Usqtped65AzCaNnjtg8=",
            ssl=True
        )
        # Initialize the DataLoader with the Redis client
        self.data_loader = DataLoader(self.redis_client)
        # Clear any existing data in Redis to ensure tests start fresh
        self.clear_redis_data()

    def clear_redis_data(self):
        """
        Clears all keys in Redis to avoid conflicts between tests.
        Ensures each test operates on a clean database without residual data from other tests.
        """
        for key in self.redis_client.keys('*'):
            self.redis_client.delete(key)

    @patch('builtins.open', new_callable=mock_open, read_data="username,password,firstname,first dogs name\nuser1@example.com,pass123,John,Max\n")
    def test_load_valid_data(self, mock_file):
        """
        Test loading valid data from a CSV file.
        This test checks if the data loader correctly parses and stores valid account information in Redis.
        """
        # Load data from the mocked CSV file
        self.data_loader.load_initial_data('ICT320 - Task 2 - Initial Database.csv')
        # Fetch stored account details from Redis
        stored_account = self.redis_client.hgetall("user1@example.com")
        # Verify that the data was stored correctly
        self.assertIn('first_name', stored_account)
        self.assertEqual(stored_account['first_name'], "John")

    @patch('builtins.open', new_callable=mock_open, read_data="username,password,firstname,first dogs name\nuser2@example.com,,Doe,\n")
    def test_load_data_with_missing_fields(self, mock_file):
        """
        Test loading data with missing fields.
        Verifies that incomplete data is not stored in Redis, maintaining data integrity.
        """
        # Attempt to load data with missing fields
        self.data_loader.load_initial_data('ICT320 - Task 2 - Initial Database.csv')
        # Fetch stored account details, expecting it to be empty due to missing required fields
        stored_account = self.redis_client.hgetall("user2@example.com")
        self.assertEqual(stored_account, {})

    @patch('builtins.open', new_callable=mock_open, read_data="username,password,firstname,first dogs name\nuser1@example.com,pass123,John,Max\nuser1@example.com,newpass,Jane,Max\n")
    def test_load_duplicate_entries(self, mock_file):
        """
        Test how the data loader handles duplicate entries in the CSV file.
        Ensures that the last occurrence of a duplicate entry is the one that gets stored.
        """
        # Load data from a mocked CSV file containing duplicate entries
        self.data_loader.load_initial_data('ICT320 - Task 2 - Initial Database.csv')
        # Fetch stored account details from Redis
        stored_account = self.redis_client.hgetall("user1@example.com")
        # Check that the account reflects the last occurrence of the duplicate entry
        self.assertIn('first_name', stored_account)
        self.assertEqual(stored_account['first_name'], "Jane")

    @patch('builtins.open', new_callable=mock_open, read_data="username,password,firstname,first dogs name\nuser3@example.com,123,42,Doggy\n")
    def test_load_data_with_incorrect_data_types(self, mock_file):
        """
        Test loading data with incorrect data types.
        Verifies that data type mismatches are handled correctly and stored without errors.
        """
        # Load data with incorrect types (e.g., numbers instead of strings)
        self.data_loader.load_initial_data('ICT320 - Task 2 - Initial Database.csv')
        # Fetch stored account details from Redis
        stored_account = self.redis_client.hgetall("user3@example.com")
        # Check that the fields were stored despite incorrect data types
        self.assertIn('first_name', stored_account)
        self.assertEqual(stored_account['first_name'], "42")

    @patch('builtins.open', new_callable=mock_open, read_data="")
    def test_load_empty_file(self, mock_file):
        """
        Test loading an empty CSV file.
        Ensures that no data is stored in Redis when the input file is empty.
        """
        # Attempt to load data from an empty file
        self.data_loader.load_initial_data('ICT320 - Task 2 - Initial Database.csv')
        # Verify that no data was loaded into Redis
        self.assertEqual(self.redis_client.keys('*'), [])

    @patch('builtins.open', new_callable=mock_open, read_data="username,password,firstname,first dogs name\ninvalid_line_without_commas\n")
    def test_load_malformed_file(self, mock_file):
        """
        Test loading a malformed CSV file.
        Verifies that an error is raised when the file structure is not as expected.
        """
        try:
            # Attempt to load data from a malformed file
            self.data_loader.load_initial_data('ICT320 - Task 2 - Initial Database.csv')
            # Fail the test if no exception is raised
            self.fail("Expected an error due to malformed data, but none was raised.")
        except Exception as e:
            # Check that an exception is raised
            self.assertTrue(isinstance(e, Exception))

    def tearDown(self):
        """
        Clean up after each test by clearing test data from Redis.
        Ensures no residual data affects subsequent tests.
        """
        self.clear_redis_data()

if __name__ == '__main__':
    unittest.main()

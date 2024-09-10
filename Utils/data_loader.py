import csv
import bcrypt

class DataLoader: #NOTE test CSV data is in Assets folder, drag to root folder to test. 
    """
    A class for loading and managing data in Redis from a CSV file.
    """

    def __init__(self, redis_client):
        """
        Initializes the DataLoader with a Redis client.

        Args:
            redis_client (redis.Redis): Redis client for database operations.
        """
        self.redis_client = redis_client

    def load_initial_data(self, csv_file):
        """
        Loads initial test data from a CSV file into Redis.

        Args:
            csv_file (str): Path to the CSV file containing initial data.
        """
        try:
            with open(csv_file, mode='r') as file:
                reader = csv.DictReader(file)
                expected_headers = ['username', 'password', 'firstname', 'first dogs name']

                # Verify that CSV headers match the expected schema
                if reader.fieldnames != expected_headers:
                    raise ValueError("CSV headers do not match the expected schema.")

                for row in reader:
                    username = row.get('username').strip()
                    password = row.get('password').strip()
                    firstname = row.get('firstname').strip()
                    first_dogs_name = row.get('first dogs name').strip()

                    # Ensure all required fields are present before saving to Redis
                    if username and password and firstname and first_dogs_name:
                        # Hash the password before storing it in Redis
                        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

                        # Prepare the mapping dictionary for Redis storage
                        data_mapping = {
                            'password': hashed_password.decode('utf-8'),
                            'first_name': firstname,
                            'security_answer': first_dogs_name
                        }

                        # Store the account details in Redis
                        self.redis_client.hset(username, mapping=data_mapping)
                    else:
                        print(f"Skipping row with missing data: {row}")

            print("Initial data loaded into Redis.")
        except FileNotFoundError:
            print(f"File not found: {csv_file}")
        except Exception as e:
            print(f"An error occurred while loading data: {e}")

    def clear_redis_data(self):
        """
        Clears all data from Redis. Use with caution.
        """
        try:
            self.redis_client.flushdb()
            print("All data cleared from Redis.")
        except Exception as e:
            print(f"Failed to clear data from Redis: {e}")

    def load_data_with_handling(self, csv_file):
        """
        Loads data from a CSV file into Redis with additional row-level error handling.

        Args:
            csv_file (str): Path to the CSV file containing data.
        """
        try:
            with open(csv_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        username = row.get('username').strip()
                        password = row.get('password').strip()
                        firstname = row.get('firstname').strip()
                        first_dogs_name = row.get('first dogs name').strip()

                        # Hash the password and save valid rows to Redis
                        if username and password and firstname and first_dogs_name:
                            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                            self.redis_client.hset(username, mapping={
                                'password': hashed_password.decode('utf-8'),
                                'first_name': firstname,
                                'security_answer': first_dogs_name
                            })
                        else:
                            print(f"Skipping row with missing fields: {row}")
                    except Exception as row_error:
                        print(f"Error processing row {row}: {row_error}")

            print("Data loaded with additional error handling.")
        except Exception as e:
            print(f"Error loading data: {e}")

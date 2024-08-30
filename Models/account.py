# models/account.py

import bcrypt

class Account:
    def __init__(self, redis_client):
        """
        Initializes the Account manager with a Redis client.
        
        Args:
            redis_client (redis.Redis): Redis client for database operations.
        """
        self.redis_client = redis_client

    def create_account(self, login_name, password, first_name):
        """
        Creates a new user account in Redis with custom security question.
        
        Args:
            login_name (str): The user's login name.
            password (str): The user's password.
            first_name (str): The user's first name.
        """
        if self.redis_client.exists(login_name):
            print("Account already exists.")
        else:
            # Ask for a custom security question
            security_question = input("Enter your custom security question: ").strip()
            security_answer = input(f"{security_question} ").strip()
            
            # Hash the password before storing it
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # Store the account details in Redis without encrypting the security answer
            self.redis_client.hset(login_name, mapping={
                'password': hashed_password.decode('utf-8'),  # Store as string
                'first_name': first_name,
                'security_question': security_question,
                'security_answer': security_answer  # Store as plain text
            })
            print("Account created successfully.")

    def login(self, login_name, password):
        """
        Validates the user's login credentials.
        
        Args:
            login_name (str): The user's login name.
            password (str): The user's password.
            
        Returns:
            bool: True if login is successful, False otherwise.
        """
        if self.redis_client.exists(login_name):
            stored_password = self.redis_client.hget(login_name, 'password')
            # Convert stored password back to bytes for bcrypt
            stored_password = stored_password.encode('utf-8')  # Convert back to bytes
            # Verify the hashed password
            if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                print("Login successful!")
                return True
            else:
                print("Incorrect password.")
                return False
        else:
            print("Account does not exist.")
            return False

    def forgot_password(self, login_name):
        """
        Handles password recovery using a custom security question.

        Args:
            login_name (str): The user's login name.

        Returns:
            bool: True if password reset is successful, False otherwise.
        """
        if self.redis_client.exists(login_name):
            # Retrieve the security question directly as a string
            security_question = self.redis_client.hget(login_name, 'security_question')
            stored_security_answer = self.redis_client.hget(login_name, 'security_answer')

            # Ask the stored security question
            user_answer = input(f"{security_question} ").strip()

            # Verify the security answer
            if user_answer == stored_security_answer:
                new_password = input("Enter your new password: ").strip()
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                self.redis_client.hset(login_name, 'password', hashed_password)
                print("Password updated successfully.")
                return True
            else:
                print("Incorrect security answer.")
                return False
        else:
            print("Account does not exist.")
            return False

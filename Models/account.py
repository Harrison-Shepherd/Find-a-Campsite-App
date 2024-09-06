import bcrypt
import re

class Account:
    def __init__(self, redis_client):
        """
        Initializes the Account manager with a Redis client.
        
        Args:
            redis_client (redis.Redis): Redis client for database operations.
        """
        self.redis_client = redis_client

    def create_account(self, login_name, password, first_name, security_question=None, security_answer=None):
        """
        Creates a new user account in Redis with custom security question.
        
        Args:
            login_name (str): The user's login name or email.
            password (str): The user's password.
            first_name (str): The user's first name.
            security_question (str, optional): The custom security question provided by the user.
            security_answer (str, optional): The answer to the custom security question.
        """
        # Check if the provided login name is a valid email address
        if not self.is_valid_email(login_name):
            print("Invalid email format. Please enter a valid email address.")
            return

        if self.redis_client.exists(login_name):
            print("Account already exists.")
        else:
            # If no security question is provided, prompt the user (CLI compatibility)
            if not security_question:
                security_question = input("Enter your custom security question: ").strip()
            
            # Ensure the security question ends with a question mark
            if not security_question.endswith('?'):
                security_question += '?'

            # If no security answer is provided, prompt the user (CLI compatibility)
            if not security_answer:
                security_answer = input(f"{security_question} ").strip()
            
            # Hash the password before storing it
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # Store the account details in Redis
            self.redis_client.hset(login_name, mapping={
                'password': hashed_password.decode('utf-8'),
                'first_name': first_name,
                'security_question': security_question,
                'security_answer': security_answer
            })
            print("Account created successfully.")

    def is_valid_email(self, email):
        """
        Validates the email format.
        
        Args:
            email (str): The email address to validate.
        
        Returns:
            bool: True if email is valid, False otherwise.
        """
        return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

    def login(self, login_name, password):
        """
        Handles user login by verifying the provided credentials against stored data in Redis.

        Args:
            login_name (str): The email or username provided by the user for login.
            password (str): The password provided by the user.

        Returns:
            bool: True if login is successful, otherwise False.
        """

        # Trim spaces from the login_name to avoid accidental input errors; do not alter the password.
        login_name = login_name.strip()
        
        print(f"Attempting to log in with: '{login_name}'")

        # Check if an account exists for the provided login name in Redis.
        if self.redis_client.exists(login_name):
            print(f"Found account for: '{login_name}'")

            # Retrieve the stored password hash from Redis and ensure it is in byte format for bcrypt.
            stored_password = self.redis_client.hget(login_name, 'password').encode('utf-8')
            
            # Verify the provided password against the stored hash using bcrypt.
            # bcrypt.checkpw() returns True if the password matches, otherwise False.
            if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                print("Login successful!")
                return True
            else:
                # If the provided password does not match the stored password, return False.
                print("Incorrect password.")
                return False
        else:
            # If no account is found for the provided login name, notify the user.
            print(f"Account for '{login_name}' does not exist.")
            return False



    def forgot_password(self, login_name, user_answer, new_password, confirm_password):
        """
        Handles password recovery using a custom security question.

        Args:
            login_name (str): The user's login name.
            user_answer (str): The user's answer to the security question.
            new_password (str): The new password provided by the user.
            confirm_password (str): Confirmation of the new password.

        Returns:
            bool: True if password reset is successful, otherwise False.
        """
        if self.redis_client.exists(login_name):
            # Retrieve the security question and answer from Redis
            stored_security_answer = self.redis_client.hget(login_name, 'security_answer')

            # Decode the stored answer if it is in bytes
            if isinstance(stored_security_answer, bytes):
                stored_security_answer = stored_security_answer.decode('utf-8')

            # Validate that the security answer exists
            if not stored_security_answer:
                print("Security question or answer not set up correctly.")
                return False

            # Compare the user's answer with the stored answer
            if user_answer == stored_security_answer:
                # Check if the new passwords match
                if new_password != confirm_password:
                    print("Passwords do not match. Try again.")
                    return False

                # Hash the new password and update it in Redis
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                self.redis_client.hset(login_name, mapping={'password': hashed_password.decode('utf-8')})
                print("Password updated successfully.")
                return True
            else:
                print("Incorrect security answer.")
                return False
        else:
            print("Account does not exist.") 
            return False


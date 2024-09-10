import bcrypt
import re

class Account:
    """
    Manages user account operations including creation, login, and password recovery.
    """

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
        if not self.is_valid_email(login_name):
            print("Invalid email format. Please enter a valid email address.")
            return

        if self.redis_client.exists(login_name):
            print("Account already exists.")
        else:
            # Prompt for security question and answer if not provided
            if not security_question:
                security_question = input("Enter your custom security question: ").strip()
            
            # Ensure the security question ends with a question mark
            if not security_question.endswith('?'):
                security_question += '?'

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
        login_name = login_name.strip()
        
        # Check if an account exists for the provided login name
        if self.redis_client.exists(login_name):
            # Retrieve the stored password hash from Redis
            stored_password = self.redis_client.hget(login_name, 'password').encode('utf-8')
            
            # Verify the provided password against the stored hash
            if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                print("Login successful!")
                return True
            else:
                print("Incorrect password.")
                return False
        else:
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
            # Retrieve the security answer from Redis
            stored_security_answer = self.redis_client.hget(login_name, 'security_answer')

            # Decode the stored answer if it is in bytes
            if isinstance(stored_security_answer, bytes):
                stored_security_answer = stored_security_answer.decode('utf-8')

            if not stored_security_answer:
                print("Security question or answer not set up correctly.")
                return False

            # Verify the provided security answer
            if user_answer == stored_security_answer:
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

import bcrypt
from Models.redis_client import RedisClient
from Models.account import Account
from Utils.data_loader import DataLoader
from GUI.gui_helpers import show_popup

class AppLogic:
    """
    Main application logic handling account management and data operations.
    """

    def __init__(self):
        """
        Initializes the application logic by setting up the Redis client and account manager.
        """
        try:
            # Initialize Redis client with connection details and set up account manager
            self.redis_client = RedisClient(
                host='mycampsiteredis.redis.cache.windows.net',
                port=6380,
                password='F21P4lrm3B63A5nNWUldt528Usqtped65AzCaNnjtg8=',
                ssl=True
            ).client
            self.account_manager = Account(self.redis_client)

            # Load initial data if needed #NOTE CSV data is not in the root folder, if you want to test on that, take it out of the Assets folder, this is due to a startup lag from encryption the CSV data and fixing the security questions. No lag if you dont load the csv
            self.load_initial_data()

        except Exception as e: 
            show_popup("Connection Error", f"Failed to connect to Redis: {e}")

    def load_initial_data(self):
        """
        Loads initial test data into Redis from a CSV file for testing purposes. NOTE it is currently in Assets, drag into root next to gui_main.py to test.
        """
        try:
            data_loader = DataLoader(self.redis_client)
            data_loader.load_initial_data('ICT320 - Task 2 - Initial Database.csv')
            print("Initial data loaded into Redis successfully.")
        except FileNotFoundError:
            print("CSV file not found. Ensure the file path is correct.")
        except Exception as e:
            print(f"Error loading initial data: {e}")

    def create_account(self, login_name, password, first_name, security_question, security_answer):
        """
        Handles the creation of a new account.

        Args:
            login_name (str): The user's login name or email.
            password (str): The user's password.
            first_name (str): The user's first name.
            security_question (str): The custom security question.
            security_answer (str): The answer to the security question.

        Returns:
            tuple: (bool, str) - Success status and message.
        """
        if not all([login_name, password, first_name, security_question, security_answer]):
            return False, "All fields are required."

        try:
            # Check if the account already exists
            if self.redis_client.hexists(login_name, 'password'):
                return False, "Account already exists."

            # Create the new account
            self.account_manager.create_account(login_name, password, first_name, security_question, security_answer)
            return True, "Account created successfully."

        except Exception as e:
            return False, f"Failed to create account: {str(e)}"

    def login(self, login_name, password):
        """
        Handles user login by validating credentials.

        Args:
            login_name (str): The user's login name or email.
            password (str): The user's password.

        Returns:
            tuple: (bool, str) - Success status and message.
        """
        if not login_name or not password:
            return False, "Login name and password required."

        if self.account_manager.login(login_name, password):
            return True, "Login successful!"
        else:
            return False, "Incorrect login credentials."

    def handle_forgot_password(self, login_name):
        """
        Retrieves the security question for password reset.

        Args:
            login_name (str): The user's login name or email.

        Returns:
            tuple: (str, str) - The security question and an error message if applicable.
        """
        if not login_name:
            return None, "Login name is required."

        # Grabs the security question from Redis
        security_question = self.redis_client.hget(login_name, 'security_question')
        security_answer = self.redis_client.hget(login_name, 'security_answer')

        if not self.redis_client.exists(login_name):
            return None, "Account does not exist."

        # Provide a default security question if none is set NOTE this is for test data
        if not security_question and security_answer:
            security_question = "What is the name of your first pet?"  # Default question

        if security_question:
            return security_question, None
        else:
            return None, "Account does not exist or security question not set up."

    def verify_security_answer(self, login_name, user_answer):
        """
        Verifies the user's answer to the stored security question.

        Args:
            login_name (str): The user's login name or email.
            user_answer (str): The answer provided by the user.

        Returns:
            bool: True if the answer is correct, False otherwise.
        """
        login_name = login_name.strip()
        user_answer = user_answer.strip()
        
        stored_answer = self.redis_client.hget(login_name, 'security_answer')
        if stored_answer and stored_answer.strip() == user_answer:
            return True
        else:
            show_popup("Error", "Incorrect security answer.")
            return False

    def reset_password(self, login_name, new_password):
        """
        Resets the user's password.

        Args:
            login_name (str): The user's login name or email.
            new_password (str): The new password provided by the user.

        Returns:
            tuple: (bool, str) - Success status and message.
        """
        try:
            # Hash the new password and update it in Redis
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            self.redis_client.hset(login_name, mapping={'password': hashed_password.decode('utf-8')})
            return True, "Password updated successfully."
        except Exception as e:
            return False, f"Failed to reset password: {e}"

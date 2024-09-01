import bcrypt
from Models.redis_client import RedisClient
from Models.account import Account
from Utils.data_loader import DataLoader
from GUI.gui_helpers import show_popup  # Ensure correct import of the show_popup function

class AppLogic:
    def __init__(self):
        # Initialize Redis Client and Account Manager
        try:
            self.redis_client = RedisClient(
                host='mycampsiteredis.redis.cache.windows.net',
                port=6380,
                password='F21P4lrm3B63A5nNWUldt528Usqtped65AzCaNnjtg8=',
                ssl=True
            ).client
            self.account_manager = Account(self.redis_client)

            # Load initial data from CSV (optional)
            self.load_initial_data()

        except Exception as e:
            show_popup("Connection Error", f"Failed to connect to Redis: {e}")

    def load_initial_data(self):
        """
        Loads initial data into Redis from a CSV file for testing.
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
        Handles account creation logic.
        """
        if not all([login_name, password, first_name, security_question, security_answer]):
            return False, "All fields are required."

        try:
            # Check if account already exists
            if self.redis_client.hexists(login_name, 'password'):
                return False, "Account already exists."

            # Proceed with account creation
            self.account_manager.create_account(login_name, password, first_name, security_question, security_answer)
            return True, "Account created successfully."

        except Exception as e:
            return False, f"Failed to create account: {str(e)}"

    def login(self, login_name, password):
        """
        Handles login logic.
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
        """
        if not login_name:
            return None, "Login name is required."

        # Fetch the security question from Redis
        security_question = self.redis_client.hget(login_name, 'security_question')
        if security_question:
            return security_question, None  # Return the question and no error message
        else:
            return None, "Account does not exist or security question not set up."

    def verify_security_answer(self, login_name, user_answer):
        """
        Verifies the user's answer to the security question.
        """
        stored_answer = self.redis_client.hget(login_name, 'security_answer')
        if stored_answer and stored_answer == user_answer:
            return True
        else:
            show_popup("Error", "Incorrect security answer.")
            return False

    def reset_password(self, login_name, new_password):
        """
        Resets the user's password.
        """
        try:
            # Hash the new password and update it in Redis
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            self.redis_client.hset(login_name, mapping={'password': hashed_password.decode('utf-8')})
            return True, "Password updated successfully."
        except Exception as e:
            return False, f"Failed to reset password: {e}"
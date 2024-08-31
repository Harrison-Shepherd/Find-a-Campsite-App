# GUI/gui_logic.py

from tkinter import messagebox
from Models.redis_client import RedisClient
from Models.account import Account
from Utils.data_loader import DataLoader


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

            # Load initial data from CSV (no pop-up)
            self.load_initial_data()

        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect to Redis: {e}")

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
            messagebox.showerror("Error", "All fields are required.")
            return False

        try:
            self.account_manager.create_account(login_name, password, first_name, security_question, security_answer)
            messagebox.showinfo("Success", "Account created successfully.")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create account: {e}")
            return False

    def login(self, login_name, password):
        """
        Handles login logic.
        """
        if not login_name or not password:
            messagebox.showerror("Error", "Login name and password are required.")
            return False

        if self.account_manager.login(login_name, password):
            messagebox.showinfo("Login", "Login successful!")
            return True
        else:
            messagebox.showerror("Login Failed", "Incorrect login credentials.")
            return False

    def forgot_password(self, login_name):
        """
        Handles the retrieval of the security question for password reset.
        """
        if not login_name:
            messagebox.showerror("Error", "Login name is required.")
            return None

        # Fetch the security question from Redis
        security_question = self.redis_client.hget(login_name, 'security_question')
        if security_question:
            return security_question  # No need to decode; it's already a string
        else:
            messagebox.showerror("Error", "Account does not exist or security question not set up.")
            return None


    def reset_password(self, login_name, security_answer, new_password, confirm_password):
        """
        Handles the actual password reset process.
        """
        if not all([login_name, security_answer, new_password, confirm_password]):
            messagebox.showerror("Error", "All fields are required.")
            return False

        if new_password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return False

        if self.account_manager.forgot_password(login_name, security_answer, new_password, confirm_password):
            messagebox.showinfo("Success", "Password updated successfully.")
            return True
        else:
            messagebox.showerror("Error", "Failed to reset password. Please check your security answer and try again.")
            return False

    def handle_forgot_password(self, login_name):
        """
        Handles the entire forgot password flow from fetching the security question to resetting the password.
        """
        security_question = self.forgot_password(login_name)
        if security_question:
            return security_question
        return None

    def handle_reset_password(self, login_name, security_answer, new_password, confirm_password):
        """
        Completes the password reset process.
        """
        return self.reset_password(login_name, security_answer, new_password, confirm_password)

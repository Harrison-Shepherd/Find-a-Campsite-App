# GUI/gui_visuals.py

import tkinter as tk
from tkinter import ttk
from gui_logic import AppLogic


class AppVisuals:
    def __init__(self, root):
        self.root = root
        self.logic = AppLogic()  # Initialize logic
        self.root.title("Find a Campsite App")
        self.root.geometry("400x500")
        self.root.configure(bg='#f0f0f0')  # Set background color

        self.create_widgets()

    def create_widgets(self):
        # Create a frame for the buttons
        button_frame = ttk.Frame(self.root, padding="10", style="Custom.TFrame")
        button_frame.pack(pady=100)

        # Style the buttons
        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 12), padding=5)
        style.configure('Custom.TFrame', background='#f0f0f0')

        # Buttons for Create Account, Login, Forgot Password, and Exit
        ttk.Button(button_frame, text="Create Account", command=self.create_account_view).pack(pady=10)
        ttk.Button(button_frame, text="Login", command=self.login_view).pack(pady=10)
        ttk.Button(button_frame, text="Forgot Password", command=self.forgot_password_view).pack(pady=10)
        ttk.Button(button_frame, text="Exit", command=self.root.quit).pack(pady=10)

        # Frame to hold the dynamic content (entry forms)
        self.form_frame = ttk.Frame(self.root, padding="10", style="Custom.TFrame")
        self.form_frame.pack(pady=10)

    def clear_form(self):
        # Clear existing widgets in the form_frame
        for widget in self.form_frame.winfo_children():
            widget.destroy()

    def create_account_view(self):
        self.clear_form()

        ttk.Label(self.form_frame, text="Create Account", font=('Helvetica', 14)).pack(pady=5)

        # Input fields for account creation
        self.create_entry_field("Enter login name (email):", 'login')
        self.create_entry_field("Enter password:", 'password', show='*')
        self.create_entry_field("Enter your first name:", 'first_name')
        self.create_entry_field("Enter your custom security question:", 'security_question')
        self.create_entry_field("Enter the answer to your security question:", 'security_answer')

        submit_button = ttk.Button(self.form_frame, text="Submit", command=self.handle_create_account)
        submit_button.pack(pady=20)

    def create_entry_field(self, label_text, var_name, show=None):
        """
        Creates a labeled entry field and assigns the Entry widget to a variable in the instance.
        """
        ttk.Label(self.form_frame, text=label_text).pack(pady=5)
        entry = ttk.Entry(self.form_frame, show=show) if show else ttk.Entry(self.form_frame)
        entry.pack()
        setattr(self, f"{var_name}_entry", entry)

    def handle_create_account(self):
        login_name = self.login_entry.get()
        password = self.password_entry.get()
        first_name = self.first_name_entry.get()
        security_question = self.security_question_entry.get()
        security_answer = self.security_answer_entry.get()

        # Call the create_account method from logic
        self.logic.create_account(login_name, password, first_name, security_question, security_answer)

    def login_view(self):
        self.clear_form()

        ttk.Label(self.form_frame, text="Login", font=('Helvetica', 14)).pack(pady=5)

        self.create_entry_field("Enter login name (email):", 'login')
        self.create_entry_field("Enter password:", 'password', show='*')

        submit_button = ttk.Button(self.form_frame, text="Submit", command=self.handle_login)
        submit_button.pack(pady=20)

    def handle_login(self):
        login_name = self.login_entry.get()
        password = self.password_entry.get()

        # Call the login method from logic
        self.logic.login(login_name, password)

    def forgot_password_view(self):
        self.clear_form()

        ttk.Label(self.form_frame, text="Forgot Password", font=('Helvetica', 14)).pack(pady=5)

        self.create_entry_field("Enter login name (email):", 'login')

        submit_button = ttk.Button(self.form_frame, text="Submit", command=self.handle_forgot_password)
        submit_button.pack(pady=20)

    def handle_forgot_password(self):
        login_name = self.login_entry.get()
        
        # Retrieve the security question and display it
        security_question = self.logic.forgot_password(login_name)

        if security_question:
            # If security question exists, proceed to prompt user for the answer
            self.clear_form()

            ttk.Label(self.form_frame, text=security_question).pack(pady=5)

            self.create_entry_field("Enter your security answer:", 'security_answer')
            self.create_entry_field("Enter your new password:", 'new_password', show='*')
            self.create_entry_field("Confirm your new password:", 'confirm_password', show='*')

            submit_button = ttk.Button(self.form_frame, text="Submit", command=lambda: self.handle_reset_password(login_name))
            submit_button.pack(pady=20)

    def handle_reset_password(self, login_name):
        security_answer = self.security_answer_entry.get()
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # Perform the password reset using logic
        self.logic.reset_password(login_name, security_answer, new_password, confirm_password)

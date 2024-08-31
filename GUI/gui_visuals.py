import tkinter as tk
from tkinter import ttk
from GUI.gui_logic import AppLogic
from PIL import Image, ImageTk


class AppVisuals:
    def __init__(self, root):
        self.root = root
        self.logic = AppLogic()  # Initialize logic
        self.root.title("Find a Campsite App")
        self.root.geometry("600x700")
        self.set_favicon()
        self.create_background()
        self.create_exit_button()

        # Create main frame to switch between fragments
        self.main_frame = tk.Frame(self.canvas, bg='', bd=0, highlightthickness=0)  # Transparent frame
        self.canvas.create_window(300, 350, window=self.main_frame)

        # Show main menu initially
        self.show_main_menu()

    def set_favicon(self):
        """Set the window favicon."""
        icon = ImageTk.PhotoImage(file="Assets/favicon.png")
        self.root.iconphoto(False, icon)

    def create_background(self):
        """Create the background image."""
        bg_image = Image.open("Assets/background.jpg")
        bg_image = bg_image.resize((600, 700), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        self.canvas = tk.Canvas(self.root, width=600, height=700, bd=0, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

    def create_exit_button(self):
        """Create an always accessible exit button."""
        exit_icon = ImageTk.PhotoImage(Image.open("Assets/exit_icon.png").resize((30, 30)))
        self.exit_button = ttk.Button(self.root, image=exit_icon, command=self.show_main_menu)
        self.exit_button.image = exit_icon  # Keep a reference to prevent garbage collection
        self.exit_button.place(x=10, y=10)

    def show_main_menu(self):
        """Display the main menu with spaced buttons."""
        self.clear_frame(self.main_frame)

        # Create buttons with icons and style
        self.create_icon_button(self.main_frame, "Create Account", "Assets/create_icon.png", self.create_account_view, "#d9e6f2")
        self.create_icon_button(self.main_frame, "Login", "Assets/login_icon.png", self.login_view, "#f2d9d9")
        self.create_icon_button(self.main_frame, "Forgot Password", "Assets/forgot_icon.png", self.forgot_password_view, "#d9f2e6")
        self.create_icon_button(self.main_frame, "Info", "Assets/info_icon.png", self.show_info_view, "#f2f2d9")

    def create_icon_button(self, parent, text, icon_path, command, bg_color):
        """Create a button with an icon and text."""
        icon = ImageTk.PhotoImage(Image.open(icon_path).resize((40, 40)))
        button_frame = tk.Frame(parent, relief='solid', bd=2, bg=bg_color)  # Set the button frame with a color
        button_frame.pack(pady=10, fill='x', expand=True)

        icon_label = tk.Label(button_frame, image=icon, bd=0)  # Removed bg='' to avoid error
        icon_label.image = icon  # Keep a reference to prevent garbage collection
        icon_label.pack(side='left', padx=10)

        text_label = tk.Label(button_frame, text=text, font=('Helvetica', 12), bg=bg_color, anchor='center')
        text_label.pack(side='left', fill='both', expand=True)

        # Bind click event to the button components
        button_frame.bind("<Button-1>", lambda e: command())
        icon_label.bind("<Button-1>", lambda e: command())
        text_label.bind("<Button-1>", lambda e: command())


    def clear_frame(self, frame):
        """Clear all widgets from a frame."""
        for widget in frame.winfo_children():
            widget.destroy()

    def create_account_view(self):
        """Show the Create Account screen."""
        self.clear_frame(self.main_frame)
        ttk.Label(self.main_frame, text="Create Account", font=('Helvetica', 14)).pack(pady=5)
        self.create_entry_field("Enter login name (email):", 'login')
        self.create_entry_field("Enter password:", 'password', show='*')
        self.create_entry_field("Enter your first name:", 'first_name')
        self.create_entry_field("Enter your custom security question:", 'security_question')
        self.create_entry_field("Enter the answer to your security question:", 'security_answer')
        submit_button = ttk.Button(self.main_frame, text="Submit", command=self.handle_create_account)
        submit_button.pack(pady=20)

    def create_entry_field(self, label_text, var_name, show=None):
        """Create labeled entry fields."""
        ttk.Label(self.main_frame, text=label_text).pack(pady=5)
        entry = ttk.Entry(self.main_frame, show=show) if show else ttk.Entry(self.main_frame)
        entry.pack()
        setattr(self, f"{var_name}_entry", entry)

    def handle_create_account(self):
        """Handle account creation."""
        login_name = self.login_entry.get()
        password = self.password_entry.get()
        first_name = self.first_name_entry.get()
        security_question = self.security_question_entry.get()
        security_answer = self.security_answer_entry.get()
        self.logic.create_account(login_name, password, first_name, security_question, security_answer)

    def login_view(self):
        """Show the Login screen."""
        self.clear_frame(self.main_frame)
        ttk.Label(self.main_frame, text="Login", font=('Helvetica', 14)).pack(pady=5)
        self.create_entry_field("Enter login name (email):", 'login')
        self.create_entry_field("Enter password:", 'password', show='*')
        submit_button = ttk.Button(self.main_frame, text="Submit", command=self.handle_login)
        submit_button.pack(pady=20)

    def handle_login(self):
        """Handle login action."""
        login_name = self.login_entry.get()
        password = self.password_entry.get()
        self.logic.login(login_name, password)

    def forgot_password_view(self):
        """Show the Forgot Password screen."""
        self.clear_frame(self.main_frame)
        ttk.Label(self.main_frame, text="Forgot Password", font=('Helvetica', 14)).pack(pady=5)
        self.create_entry_field("Enter login name (email):", 'login')
        submit_button = ttk.Button(self.main_frame, text="Submit", command=self.handle_forgot_password)
        submit_button.pack(pady=20)

    def handle_forgot_password(self):
        """Handle forgot password action."""
        login_name = self.login_entry.get()
        security_question = self.logic.handle_forgot_password(login_name)
        if security_question:
            self.clear_frame(self.main_frame)
            ttk.Label(self.main_frame, text=security_question).pack(pady=5)
            self.create_entry_field("Enter your security answer:", 'security_answer')
            self.create_entry_field("Enter your new password:", 'new_password', show='*')
            self.create_entry_field("Confirm your new password:", 'confirm_password', show='*')
            submit_button = ttk.Button(self.main_frame, text="Submit", command=lambda: self.handle_reset_password(login_name))
            submit_button.pack(pady=20)

    def handle_reset_password(self, login_name):
        """Handle reset password action."""
        security_answer = self.security_answer_entry.get()
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        self.logic.handle_reset_password(login_name, security_answer, new_password, confirm_password)

    def show_info_view(self):
        """Show the information screen explaining the login system."""
        self.clear_frame(self.main_frame)
        info_text = (
            "Welcome to the Find a Campsite App!\n\n"
            "How to use the system:\n"
            "1. Create an account using a valid email, password, and security question.\n"
            "2. Use your login credentials to access your account.\n"
            "3. Forgot your password? Use the 'Forgot Password' option to reset it using your security question."
        )
        ttk.Label(self.main_frame, text=info_text, font=('Helvetica', 12), wraplength=500).pack(pady=20)
        ttk.Button(self.main_frame, text="Back to Main Menu", command=self.show_main_menu).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = AppVisuals(root)
    root.mainloop()
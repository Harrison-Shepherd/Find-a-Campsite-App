from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.core.window import Window
from kivy.config import Config
from .gui_helpers import create_button, show_popup

# Set the window size and position
Window.size = (2000, 1440)
Window.left = (Window.width - Window.size[0]) // 2
Window.top = (Window.height - Window.size[1]) // 2
Config.set('graphics', 'position', 'custom')

class MainMenu(Screen):
    """Main Menu Screen with navigation buttons."""

    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        layout = FloatLayout()

        # Set the background image
        self.background = Image(source="Assets/background.jpg", allow_stretch=True)
        layout.add_widget(self.background)

        # Add navigation buttons with specified images
        layout.add_widget(create_button(
            "", (0.15, 0.1), {'x': 0.425, 'y': 0.55}, self.go_to_create_account, "Assets/create_icon.png"))
        layout.add_widget(create_button(
            "", (0.15, 0.1), {'x': 0.425, 'y': 0.4}, self.go_to_login, "Assets/login_icon.png"))
        layout.add_widget(create_button(
            "", (0.15, 0.1), {'x': 0.425, 'y': 0.25}, self.go_to_forgot_password, "Assets/forgot_icon.png"))

        # Add exit and help buttons
        layout.add_widget(create_button("Exit", (0.05, 0.05), {'x': 0.01, 'y': 0.93}, self.exit_app))
        layout.add_widget(create_button("", (0.05, 0.05), {'x': 0.93, 'y': 0.93}, self.go_to_info, "Assets/help_icon.png"))

        self.add_widget(layout)

    def go_to_create_account(self, instance):
        self.manager.current = 'create_account'

    def go_to_login(self, instance):
        self.manager.current = 'login'

    def go_to_forgot_password(self, instance):
        self.manager.current = 'forgot_password'

    def go_to_info(self, instance):
        self.manager.current = 'info'

    def exit_app(self, instance):
        App.get_running_app().stop()


class CreateAccountScreen(Screen):
    """Screen for creating an account."""

    def __init__(self, logic, **kwargs):
        super(CreateAccountScreen, self).__init__(**kwargs)
        self.logic = logic
        layout = FloatLayout()

        # Set the background image
        self.background = Image(source="Assets/background.jpg", allow_stretch=True)
        layout.add_widget(self.background)

        # Form layout for account creation
        form_layout = BoxLayout(orientation='vertical', padding=20, spacing=10, size_hint=(0.8, 0.6), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        form_layout.add_widget(Label(text="Create Account", font_size=32, size_hint=(1, 0.1)))

        # Input fields with write_tab set to False to navigate with Tab key
        self.login_input = TextInput(hint_text="Enter login name (email)", multiline=False, write_tab=False, size_hint=(1, 0.1), font_size=24)
        self.password_input = TextInput(hint_text="Enter password", password=True, multiline=False, write_tab=False, size_hint=(1, 0.1), font_size=24)
        self.first_name_input = TextInput(hint_text="Enter your first name", multiline=False, write_tab=False, size_hint=(1, 0.1), font_size=24)
        self.security_question_input = TextInput(hint_text="Enter your custom security question", multiline=False, write_tab=False, size_hint=(1, 0.1), font_size=24)
        self.security_answer_input = TextInput(hint_text="Enter the answer to your security question", multiline=False, write_tab=False, size_hint=(1, 0.1), font_size=24)

        # Add inputs to the form layout
        form_layout.add_widget(self.login_input)
        form_layout.add_widget(self.password_input)
        form_layout.add_widget(self.first_name_input)
        form_layout.add_widget(self.security_question_input)
        form_layout.add_widget(self.security_answer_input)

        # Add buttons for form submission and navigation
        submit_button = create_button("Submit", (1, 0.1), {}, self.handle_create_account)
        back_button = create_button("Back to Main Menu", (1, 0.1), {}, self.go_back_to_main)
        form_layout.add_widget(submit_button)
        form_layout.add_widget(back_button)

        layout.add_widget(form_layout)
        layout.add_widget(create_button("Exit", (0.05, 0.05), {'x': 0.01, 'y': 0.93}, self.exit_app))
        layout.add_widget(create_button("", (0.05, 0.05), {'x': 0.93, 'y': 0.93}, self.go_to_info, "Assets/help_icon.png"))

        self.add_widget(layout)

    def clear_inputs(self):
        """Clear all input fields."""
        self.login_input.text = ""
        self.password_input.text = ""
        self.first_name_input.text = ""
        self.security_question_input.text = ""
        self.security_answer_input.text = ""

    def handle_create_account(self, instance):
        # Gather input data and pass to the logic handler
        login_name = self.login_input.text
        password = self.password_input.text
        first_name = self.first_name_input.text
        security_question = self.security_question_input.text
        security_answer = self.security_answer_input.text
        
        success, message = self.logic.create_account(login_name, password, first_name, security_question, security_answer)

        # Show the appropriate popup based on success or failure
        show_popup("Success" if success else "Error", message)

    def go_back_to_main(self, instance):
        self.clear_inputs()  # Clear inputs when returning to the main menu
        self.manager.current = 'main'

    def exit_app(self, instance):
        App.get_running_app().stop()

    def go_to_info(self, instance):
        self.manager.current = 'info'


class LoginScreen(Screen):
    """Screen for login."""

    def __init__(self, logic, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.logic = logic
        layout = FloatLayout()

        # Set the background image
        self.background = Image(source="Assets/background.jpg", allow_stretch=True)
        layout.add_widget(self.background)

        # Form layout for login
        form_layout = BoxLayout(orientation='vertical', padding=20, spacing=10, size_hint=(0.8, 0.6), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        form_layout.add_widget(Label(text="Login", font_size=32, size_hint=(1, 0.1)))

        # Input fields for login
        self.login_input = TextInput(hint_text="Enter login name (email)", multiline=False, write_tab=False, size_hint=(1, 0.1), font_size=24)
        self.password_input = TextInput(hint_text="Enter password", password=True, multiline=False, write_tab=False, size_hint=(1, 0.1), font_size=24)

        # Add input fields and buttons to the form
        form_layout.add_widget(self.login_input)
        form_layout.add_widget(self.password_input)
        submit_button = create_button("Submit", (1, 0.1), {}, self.handle_login)
        back_button = create_button("Back to Main Menu", (1, 0.1), {}, self.go_back_to_main)
        form_layout.add_widget(submit_button)
        form_layout.add_widget(back_button)

        layout.add_widget(form_layout)
        layout.add_widget(create_button("Exit", (0.05, 0.05), {'x': 0.01, 'y': 0.93}, self.exit_app))
        layout.add_widget(create_button("", (0.05, 0.05), {'x': 0.93, 'y': 0.93}, self.go_to_info, "Assets/help_icon.png"))

        self.add_widget(layout)

    def clear_inputs(self):
        """Clear all input fields."""
        self.login_input.text = ""
        self.password_input.text = ""

    # LoginScreen class

    def handle_login(self, instance):
        # Collect data and call the login logic
        login_name = self.login_input.text
        password = self.password_input.text
        success, message = self.logic.login(login_name, password)  # Expecting a tuple return (success, message)
        show_popup("Success" if success else "Error", message)  # Show popup only once based on the message


    def go_back_to_main(self, instance):
        self.clear_inputs()  # Clear inputs when returning to the main menu
        self.manager.current = 'main'

    def exit_app(self, instance):
        App.get_running_app().stop()

    def go_to_info(self, instance):
        self.manager.current = 'info'


class ForgotPasswordScreen(Screen):
    """Screen for password reset process."""

    def __init__(self, logic, **kwargs):
        super(ForgotPasswordScreen, self).__init__(**kwargs)
        self.logic = logic
        self.stage = 1  # Stage to track the flow: 1 = email, 2 = security answer, 3 = reset password
        layout = FloatLayout()

        # Set the background image
        self.background = Image(source="Assets/background.jpg", allow_stretch=True)
        layout.add_widget(self.background)

        # Form layout
        self.form_layout = BoxLayout(orientation='vertical', padding=20, spacing=10, size_hint=(0.8, 0.6), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.title_label = Label(text="Forgot Password", font_size=32, size_hint=(1, 0.1))
        self.form_layout.add_widget(self.title_label)

        # Input fields
        self.login_input = TextInput(hint_text="Enter login name (email)", multiline=False, write_tab=False, size_hint=(1, 0.1), font_size=24)
        self.security_answer_input = TextInput(hint_text="Enter your security answer", multiline=False, write_tab=False, size_hint=(1, 0.1), font_size=24)
        self.new_password_input = TextInput(hint_text="Enter your new password", password=True, multiline=False, write_tab=False, size_hint=(1, 0.1), font_size=24)
        self.confirm_password_input = TextInput(hint_text="Confirm your new password", password=True, multiline=False, write_tab=False, size_hint=(1, 0.1), font_size=24)

        # Add the email input field initially
        self.form_layout.add_widget(self.login_input)

        # Buttons
        self.submit_button = create_button("Submit", (1, 0.1), {}, self.handle_submit)
        self.back_button = create_button("Back to Main Menu", (1, 0.1), {}, self.go_back_to_main)
        self.form_layout.add_widget(self.submit_button)
        self.form_layout.add_widget(self.back_button)

        layout.add_widget(self.form_layout)
        layout.add_widget(create_button("Exit", (0.05, 0.05), {'x': 0.01, 'y': 0.93}, self.exit_app))
        layout.add_widget(create_button("", (0.05, 0.05), {'x': 0.93, 'y': 0.93}, self.go_to_info, "Assets/help_icon.png"))

        self.add_widget(layout)

    def clear_inputs(self):
        """Clear all input fields."""
        self.login_input.text = ""
        self.security_answer_input.text = ""
        self.new_password_input.text = ""
        self.confirm_password_input.text = ""

    def remove_widget_from_parent(self, widget):
        """Remove a widget from its parent if it has one."""
        if widget.parent:
            widget.parent.remove_widget(widget)

    def handle_submit(self, instance):
        if self.stage == 1:
            # Step 1: Check email and fetch security question
            login_name = self.login_input.text
            security_question, error_message = self.logic.handle_forgot_password(login_name)

            if error_message:
                show_popup("Error", error_message)
            else:
                # Move to Stage 2: Display security question and ask for the answer
                self.stage = 2
                self.title_label.text = security_question
                self.remove_widget_from_parent(self.login_input)
                self.form_layout.clear_widgets([self.submit_button, self.back_button])
                self.form_layout.add_widget(self.security_answer_input)
                self.form_layout.add_widget(self.submit_button)
                self.form_layout.add_widget(self.back_button)

        elif self.stage == 2:
            # Step 2: Validate the security answer
            user_answer = self.security_answer_input.text
            if self.logic.verify_security_answer(self.login_input.text, user_answer):
                # Move to Stage 3: Reset password
                self.stage = 3
                self.title_label.text = "Reset Your Password"
                self.remove_widget_from_parent(self.security_answer_input)
                self.form_layout.clear_widgets([self.submit_button, self.back_button])
                self.form_layout.add_widget(self.new_password_input)
                self.form_layout.add_widget(self.confirm_password_input)
                self.form_layout.add_widget(self.submit_button)
                self.form_layout.add_widget(self.back_button)
            else:
                show_popup("Error", "Incorrect security answer.")

        elif self.stage == 3:
            # Step 3: Update the password
            new_password = self.new_password_input.text
            confirm_password = self.confirm_password_input.text
            if new_password != confirm_password:
                show_popup("Error", "Passwords do not match.")
                return

            success, message = self.logic.reset_password(self.login_input.text, new_password)
            show_popup("Success" if success else "Error", message)
            if success:
                self.go_back_to_main(None)

    def go_back_to_main(self, instance):
        self.clear_inputs()  # Clear inputs when returning to the main menu
        self.stage = 1
        self.title_label.text = "Forgot Password"

        # Remove all widgets that could potentially have parents
        self.remove_widget_from_parent(self.security_answer_input)
        self.remove_widget_from_parent(self.new_password_input)
        self.remove_widget_from_parent(self.confirm_password_input)
        self.remove_widget_from_parent(self.login_input)

        # Clear and add widgets back to form_layout
        self.form_layout.clear_widgets([self.submit_button, self.back_button])
        self.form_layout.add_widget(self.login_input)
        self.form_layout.add_widget(self.submit_button)
        self.form_layout.add_widget(self.back_button)
        self.manager.current = 'main'

    def exit_app(self, instance):
        App.get_running_app().stop()

    def go_to_info(self, instance):
        self.manager.current = 'info'


class InfoScreen(Screen):
    """Screen displaying app information."""

    def __init__(self, **kwargs):
        super(InfoScreen, self).__init__(**kwargs)
        layout = FloatLayout()
        self.background = Image(source="Assets/background.jpg", allow_stretch=True)
        layout.add_widget(self.background)

        info_text = (
            "Welcome to the Find a Campsite App!\n\n"
            "How to use the system:\n"
            "1. Create an account using a valid email, password, and security question.\n"
            "2. Use your login credentials to access your account.\n"
            "3. Forgot your password? Use the 'Forgot Password' option to reset it."
        )
        info_label = Label(text=info_text, halign='center', valign='middle', size_hint=(0.8, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout.add_widget(info_label)

        back_button = Button(text="Back to Main Menu", size_hint=(0.2, 0.1), pos_hint={'center_x': 0.5, 'y': 0.1}, on_press=self.go_back_to_main)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def go_back_to_main(self, instance):
        self.manager.current = 'main'

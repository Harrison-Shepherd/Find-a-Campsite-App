from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image  # Add this import
from kivy.app import App  # Add this import
from GUI.gui_helpers import create_button, show_popup


class ForgotPasswordScreen(Screen):
    """Screen for password reset process."""

    def __init__(self, logic, **kwargs):
        super(ForgotPasswordScreen, self).__init__(**kwargs)
        self.logic = logic
        self.stage = 1  # Stage to track the flow: 1 = email, 2 = security answer, 3 = reset password
        layout = FloatLayout()

        # Set the background image
        self.background = Image(source="Assets/background.jpg", allow_stretch=True, keep_ratio=False)
        layout.add_widget(self.background)

        # Form layout
        self.form_layout = BoxLayout(orientation='vertical', padding=20, spacing=10, size_hint=(0.8, 0.6), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.title_label = Label(text="Forgot Password", font_size=28, size_hint=(1, 0.1))
        self.form_layout.add_widget(self.title_label)

        # Input fields
        self.login_input = TextInput(hint_text="Enter login name (email)", multiline=False, write_tab=False, size_hint=(1, 0.1), font_size=20)
        self.security_answer_input = TextInput(hint_text="Enter your security answer", multiline=False, write_tab=False, size_hint=(1, 0.1), font_size=20)
        self.new_password_input = TextInput(hint_text="Enter your new password", password=True, multiline=False, write_tab=False, size_hint=(1, 0.1), font_size=20)
        self.confirm_password_input = TextInput(hint_text="Confirm your new password", password=True, multiline=False, write_tab=False, size_hint=(1, 0.1), font_size=20)

        # Add the email input field initially
        self.form_layout.add_widget(self.login_input)

        # Buttons
        self.submit_button = create_button("Submit", (1, 0.1), {}, self.handle_submit)
        self.back_button = create_button("Back to Main Menu", (1, 0.1), {}, self.go_back_to_main)
        self.form_layout.add_widget(self.submit_button)
        self.form_layout.add_widget(self.back_button)

        layout.add_widget(self.form_layout)
        layout.add_widget(create_button("Exit", (0.1, 0.05), {'x': 0.01, 'y': 0.93}, self.exit_app))
        layout.add_widget(create_button("", (0.1, 0.05), {'x': 0.93, 'y': 0.93}, self.go_to_info, "Assets/help_icon.png"))

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
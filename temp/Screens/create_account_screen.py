from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.image import Image  # Import Image here
from kivy.app import App  # Import App here
from GUI.gui_helpers import create_button, show_popup


class CreateAccountScreen(Screen):
    """Screen for creating an account."""

    def __init__(self, logic, **kwargs):
        super(CreateAccountScreen, self).__init__(**kwargs)
        self.logic = logic
        layout = FloatLayout()

        # Set the background image
        self.background = Image(source="Assets/background.jpg", allow_stretch=True, keep_ratio=False)
        layout.add_widget(self.background)

        # Form layout for account creation
        form_layout = BoxLayout(orientation='vertical', padding=20, spacing=10, size_hint=(0.8, 0.6), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        form_layout.add_widget(Label(text="Create Account", font_size=28, size_hint=(1, 0.1)))

        # Update text input fields in CreateAccountScreen
        self.login_input = TextInput(hint_text="Enter login name (email)", multiline=False, write_tab=False, size_hint=(1, 0.1), font_size=20)
        self.password_input = TextInput(hint_text="Enter password", password=True, multiline=False, write_tab=False, size_hint=(1, 0.1), font_size=20)
        self.first_name_input = TextInput(hint_text="Enter your first name", multiline=False, write_tab=False, size_hint=(1, 0.1), font_size=20)
        self.security_question_input = TextInput(hint_text="Enter your custom security question", multiline=False, write_tab=False, size_hint=(1, 0.1), font_size=20)
        self.security_answer_input = TextInput(hint_text="Enter the answer to your security question", multiline=False, write_tab=False, size_hint=(1, 0.1), font_size=20)


        # Add inputs to the form layout
        form_layout.add_widget(self.login_input)
        form_layout.add_widget(self.password_input)
        form_layout.add_widget(self.first_name_input)
        form_layout.add_widget(self.security_question_input)
        form_layout.add_widget(self.security_answer_input)

        # Add buttons for form submission and navigation
        form_layout.add_widget(create_button("Submit", (1, 0.1), {}, self.handle_create_account))
        form_layout.add_widget(create_button("Back to Main Menu", (1, 0.1), {}, self.go_back_to_main))

        layout.add_widget(form_layout)
        layout.add_widget(create_button("Exit", (0.1, 0.05), {'x': 0.01, 'y': 0.93}, self.exit_app))
        layout.add_widget(create_button("", (0.1, 0.05), {'x': 0.93, 'y': 0.93}, self.go_to_info, "Assets/help_icon.png"))

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
        show_popup("Success" if success else "Error", message)

    def go_back_to_main(self, instance):
        self.clear_inputs()  # Clear inputs when returning to the main menu
        self.manager.current = 'main'

    def exit_app(self, instance):
        App.get_running_app().stop()

    def go_to_info(self, instance):
        self.manager.current = 'info'

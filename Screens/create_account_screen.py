from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.app import App
from GUI.gui_helpers import create_button, show_popup
from GUI.gui_helpers import create_exit_button, create_help_button



class CreateAccountScreen(Screen):
    """Screen for creating a new account."""

    def __init__(self, logic, **kwargs):
        super(CreateAccountScreen, self).__init__(**kwargs)
        self.logic = logic
        layout = FloatLayout()

        # Set the background image
        self.background = Image(source="Assets/background.jpg", allow_stretch=True, keep_ratio=False)
        layout.add_widget(self.background)

        # Layout for the form inputs and buttons
        form_layout = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=10,
            size_hint=(0.8, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        form_layout.add_widget(Label(text="Create Account", font_size=28, size_hint=(1, 0.1)))

        # Input fields for creating an account
        self.login_input = TextInput(
            hint_text="Enter login name (email)",
            multiline=False,
            write_tab=False,
            size_hint=(1, 0.1),
            font_size=20
        )
        self.password_input = TextInput(
            hint_text="Enter password",
            password=True,
            multiline=False,
            write_tab=False,
            size_hint=(1, 0.1),
            font_size=20
        )
        self.first_name_input = TextInput(
            hint_text="Enter your first name",
            multiline=False,
            write_tab=False,
            size_hint=(1, 0.1),
            font_size=20
        )
        self.security_question_input = TextInput(
            hint_text="Enter your custom security question",
            multiline=False,
            write_tab=False,
            size_hint=(1, 0.1),
            font_size=20
        )
        self.security_answer_input = TextInput(
            hint_text="Enter the answer to your security question",
            multiline=False,
            write_tab=False,
            size_hint=(1, 0.1),
            font_size=20
        )

        # Add input fields to the form layout
        form_layout.add_widget(self.login_input)
        form_layout.add_widget(self.password_input)
        form_layout.add_widget(self.first_name_input)
        form_layout.add_widget(self.security_question_input)
        form_layout.add_widget(self.security_answer_input)

        # Add submit and navigation buttons
        form_layout.add_widget(create_button("Submit", (1, 0.1), {}, self.handle_create_account))
        form_layout.add_widget(create_button("Back to Main Menu", (1, 0.1), {}, self.go_back_to_main))

        # Add form layout and other navigation buttons to the main layout
        layout.add_widget(form_layout)
        # Inside the screen class, replace the button creation with the standardized functions
        layout.add_widget(create_exit_button(self.exit_app))
        layout.add_widget(create_help_button(self.go_to_info))

        self.add_widget(layout)

    def clear_inputs(self):
        """Clear all input fields in the form."""
        self.login_input.text = ""
        self.password_input.text = ""
        self.first_name_input.text = ""
        self.security_question_input.text = ""
        self.security_answer_input.text = ""

    def handle_create_account(self, instance):
        """
        Handles the account creation process by gathering input data
        and passing it to the logic handler.
        """
        login_name = self.login_input.text
        password = self.password_input.text
        first_name = self.first_name_input.text
        security_question = self.security_question_input.text
        security_answer = self.security_answer_input.text

        success, message = self.logic.create_account(login_name, password, first_name, security_question, security_answer)
        show_popup("Success" if success else "Error", message)

    def go_back_to_main(self, instance):
        """Clears inputs and navigates back to the main menu."""
        self.clear_inputs()
        self.manager.current = 'main'

    def exit_app(self, instance):
        """Exit the application."""
        App.get_running_app().stop()

    def go_to_info(self, instance):
        """Navigate to the information screen."""
        self.manager.current = 'info'

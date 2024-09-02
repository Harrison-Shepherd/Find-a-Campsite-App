from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.app import App
from GUI.gui_helpers import create_button, show_popup
from GUI.gui_helpers import create_exit_button, create_help_button


class LoginScreen(Screen):
    """
    Screen for user login.
    Allows users to enter their credentials and access the app. Also provides navigation to other sections.
    """

    def __init__(self, logic, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.logic = logic
        layout = FloatLayout()

        # Set the background image
        self.background = Image(source="Assets/background.jpg", allow_stretch=True, keep_ratio=False)
        layout.add_widget(self.background)

        # Create form layout for login inputs and buttons
        form_layout = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=10,
            size_hint=(0.8, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        form_layout.add_widget(Label(text="Login", font_size=28, size_hint=(1, 0.1)))

        # Create input fields for login
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

        # Add input fields and buttons to the form layout
        form_layout.add_widget(self.login_input)
        form_layout.add_widget(self.password_input)
        form_layout.add_widget(create_button("Submit", (1, 0.1), {}, self.handle_login))
        form_layout.add_widget(create_button("Back to Main Menu", (1, 0.1), {}, self.go_back_to_main))

        layout.add_widget(form_layout)
        # Add standardized exit and help buttons
        layout.add_widget(create_exit_button(self.exit_app))
        layout.add_widget(create_help_button(self.go_to_info))

        self.add_widget(layout)

    def handle_login(self, instance):
        """
        Process the login attempt using the provided credentials.
        """
        login_name = self.login_input.text
        password = self.password_input.text
        success, message = self.logic.login(login_name, password)
        show_popup("Success" if success else "Error", message)

    def go_back_to_main(self, instance):
        """
        Clear input fields and return to the main menu screen.
        """
        self.clear_inputs()
        self.manager.current = 'main'

    def clear_inputs(self):
        """Reset all input fields to empty."""
        self.login_input.text = ""
        self.password_input.text = ""

    def exit_app(self, instance):
        """Terminate the application."""
        App.get_running_app().stop()

    def go_to_info(self, instance):
        """Switch to the information screen."""
        self.manager.current = 'info'

from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.app import App
from GUI.gui_helpers import create_button
from GUI.gui_helpers import create_exit_button, create_help_button


class MainMenuScreen(Screen):
    """
    Main Menu Screen with navigation buttons.
    This screen serves as the entry point for the app, allowing users to navigate
    to account creation, login, forgot password, and information screens.
    """

    def __init__(self, **kwargs):
        super(MainMenuScreen, self).__init__(**kwargs)
        layout = FloatLayout()

        # Set the background image
        self.background = Image(source="Assets/background.jpg", allow_stretch=True, keep_ratio=False)
        layout.add_widget(self.background)

        # Add navigation buttons with images
        layout.add_widget(create_button(
            "", (0.15, 0.1), {'x': 0.425, 'y': 0.55}, self.go_to_create_account, "Assets/create_icon.png"))
        layout.add_widget(create_button(
            "", (0.15, 0.1), {'x': 0.425, 'y': 0.4}, self.go_to_login, "Assets/login_icon.png"))
        layout.add_widget(create_button(
            "", (0.15, 0.1), {'x': 0.425, 'y': 0.25}, self.go_to_forgot_password, "Assets/forgot_icon.png"))

        # Inside the screen class, replace the button creation with the standardized functions
        layout.add_widget(create_exit_button(self.exit_app))
        layout.add_widget(create_help_button(self.go_to_info))

        # Add the layout to the screen
        self.add_widget(layout)

    def go_to_create_account(self, instance):
        """Navigate to the Create Account screen."""
        self.manager.current = 'create_account'

    def go_to_login(self, instance):
        """Navigate to the Login screen."""
        self.manager.current = 'login'

    def go_to_forgot_password(self, instance):
        """Navigate to the Forgot Password screen."""
        self.manager.current = 'forgot_password'

    def go_to_info(self, instance):
        """Navigate to the Info screen."""
        self.manager.current = 'info'

    def exit_app(self, instance):
        """Exit the application."""
        App.get_running_app().stop()

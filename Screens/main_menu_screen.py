from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image  # Import Image here
from kivy.app import App  # Import App here
from GUI.gui_helpers import create_button


class MainMenuScreen(Screen):
    """Main Menu Screen with navigation buttons."""

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

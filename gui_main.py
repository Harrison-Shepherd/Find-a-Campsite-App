# gui_main.py

from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
from Logic.app_logic import AppLogic
from Screens.main_menu_screen import MainMenuScreen
from Screens.create_account_screen import CreateAccountScreen
from Screens.login_screen import LoginScreen
from Screens.forgot_password_screen import ForgotPasswordScreen
from Screens.info_screen import InfoScreen

# Set the application title and window properties
Window.title = "Find a Campsite App"
Window.size = (1280, 720)  # Set window size
Window.left = (Window.system_size[0] - Window.size[0]) // 2  # Center window horizontally
Window.top = (Window.system_size[1] - Window.size[1]) // 2   # Center window vertically
Window.resizable = True  # Allow window resizing

class CampsiteApp(App):
    """Main application class for managing the screens and app logic."""

    def build(self):
        """Sets up the screen manager and adds all screens to it."""
        self.logic = AppLogic()  # Initialize application logic
        self.screen_manager = ScreenManager(transition=NoTransition())  # No screen transition animations

        # Add screens to the screen manager
        self.screen_manager.add_widget(MainMenuScreen(name='main'))
        self.screen_manager.add_widget(CreateAccountScreen(self.logic, name='create_account'))
        self.screen_manager.add_widget(LoginScreen(self.logic, name='login'))
        self.screen_manager.add_widget(ForgotPasswordScreen(self.logic, name='forgot_password'))
        self.screen_manager.add_widget(InfoScreen(name='info'))

        return self.screen_manager

if __name__ == '__main__':
    CampsiteApp().run()  # Run the application

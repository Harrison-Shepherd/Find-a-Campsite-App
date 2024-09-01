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

# Set the window size (adjust these dimensions as needed to fit your screen)
Window.size = (1280, 720)  # Example size, modify as per your screen resolution

# Center the window on the screen using the correct attribute
Window.left = (Window.system_size[0] - Window.size[0]) // 2
Window.top = (Window.system_size[1] - Window.size[1]) // 2

# Allow resizing if needed
Window.resizable = True

class CampsiteApp(App):
    def build(self):
        # Initialize application logic
        self.logic = AppLogic()

        # Create the screen manager with NoTransition to disable animations
        self.screen_manager = ScreenManager(transition=NoTransition())  # Disable transitions

        # Add screens to the screen manager
        self.screen_manager.add_widget(MainMenuScreen(name='main'))
        self.screen_manager.add_widget(CreateAccountScreen(self.logic, name='create_account'))
        self.screen_manager.add_widget(LoginScreen(self.logic, name='login'))
        self.screen_manager.add_widget(ForgotPasswordScreen(self.logic, name='forgot_password'))
        self.screen_manager.add_widget(InfoScreen(name='info'))

        return self.screen_manager


if __name__ == '__main__':
    CampsiteApp().run()

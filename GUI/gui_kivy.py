from kivy.uix.screenmanager import ScreenManager
from kivy.app import App
from Logic.app_logic import AppLogic
from Screens.main_menu_screen import MainMenuScreen  # Ensure this matches the class name in main_menu_screen.py
from Screens.create_account_screen import CreateAccountScreen
from Screens.login_screen import LoginScreen
from Screens.forgot_password_screen import ForgotPasswordScreen
from Screens.info_screen import InfoScreen
from kivy.uix.screenmanager import ScreenManager, NoTransition  # Import NoTransition

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

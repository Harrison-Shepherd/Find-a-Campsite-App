# GUI/gui_main.py

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition  # Import NoTransition
from GUI.gui_kivy import MainMenu, CreateAccountScreen, LoginScreen, ForgotPasswordScreen, InfoScreen
from GUI.gui_logic import AppLogic

class CampsiteApp(App):
    def build(self):
        # Initialize application logic
        logic = AppLogic()

        # Create a ScreenManager with NoTransition to make the screen change instant
        sm = ScreenManager(transition=NoTransition())  # Set transition to NoTransition
        sm.add_widget(MainMenu(name='main'))
        sm.add_widget(CreateAccountScreen(name='create_account', logic=logic))
        sm.add_widget(LoginScreen(name='login', logic=logic))
        sm.add_widget(ForgotPasswordScreen(name='forgot_password', logic=logic))
        sm.add_widget(InfoScreen(name='info'))

        return sm

if __name__ == '__main__':
    CampsiteApp().run()

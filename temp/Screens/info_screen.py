from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image  # Add this import
from kivy.app import App  # Add this import
from kivy.uix.button import Button


class InfoScreen(Screen):
    """Screen displaying app information."""

    def __init__(self, **kwargs):
        super(InfoScreen, self).__init__(**kwargs)
        layout = FloatLayout()
        self.background = Image(source="Assets/background.jpg", allow_stretch=True)
        layout.add_widget(self.background)

        info_text = (
            "Welcome to the Find a Campsite App!\n\n"
            "How to use the system:\n"
            "1. Create an account using a valid email, password, and security question.\n"
            "2. Use your login credentials to access your account.\n"
            "3. Forgot your password? Use the 'Forgot Password' option to reset it."
        )
        info_label = Label(text=info_text, halign='center', valign='middle', size_hint=(0.8, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout.add_widget(info_label)

        back_button = Button(text="Back to Main Menu", size_hint=(0.2, 0.1), pos_hint={'center_x': 0.5, 'y': 0.1}, on_press=self.go_back_to_main)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def go_back_to_main(self, instance):
        self.manager.current = 'main'

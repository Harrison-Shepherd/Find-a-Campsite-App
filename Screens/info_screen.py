from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle

class InfoScreen(Screen):
    """Screen displaying app information."""

    def __init__(self, **kwargs):
        super(InfoScreen, self).__init__(**kwargs)
        layout = FloatLayout()

        # Set the background image
        self.background = Image(source="Assets/background.jpg", allow_stretch=True)
        layout.add_widget(self.background)

        # BoxLayout for the text with a semi-transparent background
        text_box = BoxLayout(orientation='vertical', size_hint=(0.8, 0.5), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Add a semi-transparent grey background behind the text
        with text_box.canvas.before:
            Color(0.2, 0.2, 0.2, 0.6)  # RGBA: Grey color with 60% opacity
            self.rect = Rectangle(size=text_box.size, pos=text_box.pos)

        # Bind the background size and position to the box layout
        text_box.bind(size=self._update_rect, pos=self._update_rect)

        # Add text information to the box
        info_text = (
            "Welcome to the Find a Campsite App!\n\n"
            "How to use the system:\n"
            "1. Create an account using a valid email, password, and security question.\n"
            "2. Use your login credentials to access your account.\n"
            "3. Forgot your password? Use the 'Forgot Password' option to reset it."
        )
        info_label = Label(
            text=info_text,
            halign='center',
            valign='middle',
            size_hint=(1, 1),
            color=(1, 1, 1, 1)  # Text color
        )
        text_box.add_widget(info_label)

        # Add text box to the layout
        layout.add_widget(text_box)

        # Add the back button
        back_button = Button(
            text="Back to Main Menu",
            size_hint=(0.2, 0.1),
            pos_hint={'center_x': 0.5, 'y': 0.1},
            on_press=self.go_back_to_main
        )
        layout.add_widget(back_button)

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        """Update the background rectangle size and position."""
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def go_back_to_main(self, instance):
        self.manager.current = 'main'

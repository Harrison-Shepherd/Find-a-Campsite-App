# GUI/gui_helpers.py

from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
import os

# Default button image path (ensure this path points to a valid image)
DEFAULT_BUTTON_IMAGE = "Assets/default_button.png"

def create_button(text, size_hint, pos_hint, on_press, background_normal=None):
    """
    Helper function to create a button with specified properties.

    Args:
        text (str): Text displayed on the button.
        size_hint (tuple): Size hint of the button.
        pos_hint (dict): Position hint of the button.
        on_press (function): Function to call on button press.
        background_normal (str, optional): Path to the button's background image.

    Returns:
        Button: A configured Kivy Button instance.
    """
    # Use the default image if the provided path is None or does not exist
    if not background_normal or not os.path.exists(background_normal):
        background_normal = ""

    # Create the button with a fallback color if no image is used
    return Button(
        text=text,
        size_hint=size_hint,
        pos_hint=pos_hint,
        on_press=on_press,
        background_normal=background_normal,
        background_down=background_normal,
        border=(0, 0, 0, 0),
        background_color=(0.3, 0.6, 0.9, 1) if not background_normal else (1, 1, 1, 1)  # Default color if no image
    )


def show_popup(title, message):
    """
    Helper function to display a popup with a message.

    Args:
        title (str): The title of the popup.
        message (str): The message displayed inside the popup.

    Returns:
        Popup: A configured Kivy Popup instance.
    """
    content = BoxLayout(orientation='vertical')
    content.add_widget(Label(text=message, size_hint_y=None, height=50))
    button = Button(text='OK', size_hint_y=None, height=50)
    content.add_widget(button)
    popup = Popup(title=title, content=content, size_hint=(0.5, 0.3))
    button.bind(on_press=popup.dismiss)
    popup.open()

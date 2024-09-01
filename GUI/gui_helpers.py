from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout


def create_button(
    text, 
    size_hint, 
    pos_hint, 
    callback, 
    image_path=None, 
    font_size=20, 
    background_color=(0.2, 0.6, 0.8, 1), 
    border=(0, 0, 0, 0)
):
    """
    Create a button with optional image and set styles.

    Args:
        text (str): Button text.
        size_hint (tuple): Size hint tuple (width, height).
        pos_hint (dict): Position hint dict.
        callback (function): Function to be called on button press.
        image_path (str, optional): Optional path to an image file.
        font_size (int, optional): Font size of the button text.
        background_color (tuple, optional): Background color of the button.
        border (tuple, optional): Border size.

    Returns:
        Button: Configured Button object.
    """
    button = Button(
        text=text,
        size_hint=size_hint,
        pos_hint=pos_hint,
        font_size=font_size,
        background_normal=image_path if image_path else '',
        background_down=image_path if image_path else '',
        background_color=background_color if not image_path else (1, 1, 1, 1),
        color=(1, 1, 1, 1),
        border=border
    )
    button.bind(on_press=callback)
    return button


def show_popup(title, message):
    """
    Display a popup with a given title and message.

    Args:
        title (str): Title of the popup.
        message (str): Message to display in the popup.
    """
    layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
    label = Label(text=message, halign='center', valign='middle', size_hint=(1, 0.8))
    close_button = Button(text='OK', size_hint=(1, 0.2))

    layout.add_widget(label)
    layout.add_widget(close_button)

    popup = Popup(
        title=title,
        content=layout,
        size_hint=(0.6, 0.4),
        auto_dismiss=False
    )

    close_button.bind(on_press=popup.dismiss)
    popup.open()


def create_label(text, font_size=24, color=(1, 1, 1, 1)):
    """
    Create a styled label with specified text, font size, and color.

    Args:
        text (str): Text to display in the label.
        font_size (int, optional): Size of the font.
        color (tuple, optional): Color of the text.

    Returns:
        Label: Configured Label object.
    """
    return Label(
        text=text,
        font_size=font_size,
        color=color,
        halign='center',
        valign='middle'
    )


def create_exit_button(callback):
    """
    Create a standardized Exit button.

    Args:
        callback (function): Function to be called on button press.

    Returns:
        Button: Configured Exit button.
    """
    return create_button(
        text="Exit",
        size_hint=(0.05, 0.05),
        pos_hint={'x': 0.01, 'y': 0.93},
        callback=callback,
        font_size=20  # Set desired font size
    )


def create_help_button(callback):
    """
    Create a standardized Help button.

    Args:
        callback (function): Function to be called on button press.

    Returns:
        Button: Configured Help button.
    """
    return create_button(
        text="",
        size_hint=(0.07, 0.07),
        pos_hint={'x': 0.93, 'y': 0.93},
        callback=callback,
        image_path="Assets/help_icon.png"
    )

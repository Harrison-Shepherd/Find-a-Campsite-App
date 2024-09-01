from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout


def create_button(text, size_hint, pos_hint, callback, image_path=None):
    """
    Create a button with optional image and set styles.
    :param text: Button text
    :param size_hint: Size hint tuple (width, height)
    :param pos_hint: Position hint dict
    :param callback: Function to be called on button press
    :param image_path: Optional path to an image file
    :return: Configured Button object
    """
    button = Button(
        text=text,
        size_hint=size_hint,
        pos_hint=pos_hint,
        font_size=20,  # Set an appropriate font size
        background_normal=image_path if image_path else '',  # Set image if provided
        background_down=image_path if image_path else '',  # Set down image if provided
        background_color=(0.2, 0.6, 0.8, 1) if not image_path else (1, 1, 1, 1),  # Default color if no image
        color=(1, 1, 1, 1),  # Text color
        border=(0, 0, 0, 0)  # Set border to zero for proper rendering
    )
    button.bind(on_press=callback)
    return button


def show_popup(title, message):
    """
    Display a popup with a given title and message.
    :param title: Title of the popup
    :param message: Message to display in the popup
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
    :param text: Text to display in the label
    :param font_size: Size of the font
    :param color: Color of the text
    :return: Configured Label object
    """
    return Label(
        text=text,
        font_size=font_size,
        color=color,
        halign='center',
        valign='middle'
    )

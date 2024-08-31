# GUI/gui_main.py

import tkinter as tk
from GUI.gui_visuals import AppVisuals

if __name__ == "__main__":
    root = tk.Tk()
    app = AppVisuals(root)
    root.mainloop()

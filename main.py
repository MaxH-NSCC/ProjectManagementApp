import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
import ui_main
from core import load_app_settings, AppSettings

def load_stylesheet(app, theme="light"):
    path = "style.qss" if theme == "light" else "style_dark.qss"
    try:
        with open(path, "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print(f"{path} not found. Skipping stylesheet.")

if __name__ == "__main__":
    app = QApplication([])

    font = QFont()
    font.setPointSize(11)
    app.setFont(font)

    app_settings = load_app_settings()
    if app_settings is None:
        app_settings = AppSettings()

    load_stylesheet(app, app_settings.theme)

    window = ui_main.StartupScreen()
    window.show()
    app.exec_()

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
import ui_main

def load_stylesheet(app, path="style.qss"):
    try:
        with open(path, "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("Style file not found. Skipping.")

if __name__ == "__main__":
    app = QApplication([])

    font = QFont()
    font.setPointSize(11)
    app.setFont(font)

    load_stylesheet(app)

    window = ui_main.StartupScreen()
    window.show()
    app.exec_()

import sys
from PyQt5.QtWidgets import QApplication
import ui_main

if __name__ == "__main__":
    app = QApplication([])
    # start the startup screen
    window = ui_main.StartupScreen()
    window.show()
    app.exec_()
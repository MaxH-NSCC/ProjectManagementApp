import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QDialog, QLabel, 
    QTextEdit, QLineEdit, QFormLayout
)
from PyQt5.QtCore import Qt
import ui_project

class ProjectInfoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Project")
        self.resize(350, 200)

        layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.title_edit = QLineEdit()
        self.desc_edit = QTextEdit()
        self.desc_edit.setFixedHeight(80)

        form_layout.addRow("Project Title:", self.title_edit)
        form_layout.addRow("Project Description:", self.desc_edit)

        layout.addLayout(form_layout)

        self.ok_button = QPushButton("Create Project")
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

    def get_project_info(self):
        return self.title_edit.text(), self.desc_edit.toPlainText()

class StartupScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Project Manager - Startup")
        self.resize(400, 200)

        layout = QVBoxLayout()

        self.dir_label = QLabel("Current Directory:")
        self.dir_box = QLineEdit(os.getcwd())
        self.dir_box.setReadOnly(True)

        layout.addWidget(self.dir_label)
        layout.addWidget(self.dir_box)

        # Buttons
        self.open_project_btn = QPushButton("Open Project")
        self.create_project_btn = QPushButton("Create New Project")

        self.create_project_btn.clicked.connect(self.create_project)

        layout.addWidget(self.open_project_btn)
        layout.addWidget(self.create_project_btn)

        self.setLayout(layout)

    def create_project(self):
        dialog = ProjectInfoDialog(self)
        if dialog.exec_():
            title, description = dialog.get_project_info()
            self.project_window = ui_project.ProjectScreen()
            self.project_window.show()
            self.close()

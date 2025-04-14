import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QDialog, QLabel, QTextEdit, QLineEdit, QFormLayout, QMessageBox, QListWidget, QFileDialog
from PyQt5.QtCore import Qt
from ui_project import *
from core import *

# project creation dialog box
class ProjectInfoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Project")
        self.resize(450, 250)

        layout = QVBoxLayout()

        # title and desc input
        form_layout = QFormLayout()
        self.title_edit = QLineEdit()
        self.desc_edit = QTextEdit()
        self.desc_edit.setFixedHeight(80)

        form_layout.addRow("Project Title:", self.title_edit)
        form_layout.addRow("Project Description:", self.desc_edit)

        layout.addLayout(form_layout)

        # button to confirm project creation
        self.ok_button = QPushButton("Create Project")
        self.ok_button.clicked.connect(self.accept) # check to see if the user added a title
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

    # return the entered details
    def get_project_info(self):
        return self.title_edit.text(), self.desc_edit.toPlainText()

    # ensure the user added a title before creating a project
    def accept(self):
        if not self.title_edit.text().strip():
            QMessageBox.warning(self, "Input Error", "Project title is required!")
        else:
            super().accept() # close the dialog if validation passes

class StartupScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Project Manager - Startup")
        self.resize(500, 250) #400
        self.project_manager = ProjectManager()
        # self.current_directory = os.getcwd()  # OLD
        app_dir = os.path.dirname(os.path.abspath(__file__))
        default_projects_dir = os.path.join(app_dir, "Projects")
        os.makedirs(default_projects_dir, exist_ok=True)
        self.current_directory = default_projects_dir

        layout = QVBoxLayout()

        # Selectable directory input
        dir_layout = QVBoxLayout()
        self.dir_label = QLabel("Project Directory:")
        self.dir_box = QLineEdit(self.current_directory)
        self.dir_box.setReadOnly(True)
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.select_directory)

        dir_layout.addWidget(self.dir_label)
        dir_layout.addWidget(self.dir_box)
        dir_layout.addWidget(self.browse_button)

        layout.addLayout(dir_layout)

        # Project list
        self.project_list = QListWidget()
        layout.addWidget(self.project_list)

        self.open_project_btn = QPushButton("Open Project")
        self.create_project_btn = QPushButton("Create New Project")

        self.create_project_btn.clicked.connect(self.create_project)
        self.open_project_btn.clicked.connect(self.open_project)

        layout.addWidget(self.open_project_btn)
        layout.addWidget(self.create_project_btn)

        self.setLayout(layout)

        # Load initial directory
        self.load_project_list()

    # Opens a file dialog to select a project directory
    def select_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Project Directory")
        if dir_path:
            self.current_directory = dir_path
            self.dir_box.setText(dir_path)
            self.load_project_list()

    # Loads all JSON files in the selected directory into the list
    def load_project_list(self):
        self.project_list.clear()
        if not os.path.exists(self.current_directory):
            return

        for file in os.listdir(self.current_directory):
            if file.endswith(".json"):
                self.project_list.addItem(file)  # Show file names

    # Opens a selected project JSON file and loads it into memory
    def open_project(self):
        selected_item = self.project_list.currentItem()
        if selected_item:
            file_name = selected_item.text()
            file_path = os.path.join(self.current_directory, file_name)

            project = load_json(file_path)
            if project:

                core.loaded = True
                self.project_window = ProjectScreen(project, file_path)
                self.project_window.show()
                self.close()
            else:
                QMessageBox.warning(self, "Error", "Failed to load project.")

    # Creates a new project in memory but does not save it yet
    def create_project(self):
        dialog = ProjectInfoDialog(self)
        if dialog.exec_():
            title, description = dialog.get_project_info()

            if title:
                project = self.project_manager.create_project(title, description)  # Create in memory
                self.project_list.addItem(f"{title} (Unsaved)")  # Indicate it's not saved

                core.loaded = False
                self.project_window = ProjectScreen(project)
                self.project_window.show()
                self.close()
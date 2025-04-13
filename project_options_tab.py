from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit, QCheckBox, QPushButton, QLabel, QMessageBox
from PyQt5.QtGui import QIntValidator
class ProjectOptionsTab(QWidget):
    def __init__(self, project, parent=None):
        super().__init__(parent)
        self.project = project
        layout = QFormLayout()

        self.project_title = QLineEdit(self.project.title)
        self.project_description = QTextEdit(self.project.description)
        self.project_description.setMaximumHeight(200)

        self.task_delete_warning = QCheckBox("Show Warning when deleting tasks")
        self.res_delete_warning = QCheckBox("Show Warning when deleting resources")
        self.task_delete_warning.setChecked(self.project.settings.remove_task_warn)
        self.res_delete_warning.setChecked(self.project.settings.remove_res_warn)

        self.reset_button = QPushButton("Reset Settings")
        self.reset_button.clicked.connect(self.reset_settings)

        self.update_button = QPushButton("Update Settings")
        self.update_button.clicked.connect(self.update_settings)

        self.height_edit = QLineEdit(str(self.project.settings.default_height))
        self.height_edit.setValidator(QIntValidator(1, 9999, self))

        self.width_edit = QLineEdit(str(self.project.settings.default_width))
        self.width_edit.setValidator(QIntValidator(1, 9999, self))

        self.start_max = QCheckBox("Start window maximized")
        self.start_max.setChecked(self.project.settings.start_maximized)

        layout.addRow("Project Title:", self.project_title)
        layout.addRow("Project Description:", self.project_description)
        layout.addWidget(self.task_delete_warning)
        layout.addWidget(self.res_delete_warning)
        layout.addWidget(QLabel("Default App Height"))
        layout.addWidget(self.height_edit)
        layout.addWidget(QLabel("Default App Width"))
        layout.addWidget(self.width_edit)
        layout.addWidget(self.start_max)
        layout.addWidget(self.update_button)
        layout.addWidget(self.reset_button)

        self.setLayout(layout)

    def reset_settings(self):
        new_title = self.project.title
        new_description = self.project.description
        new_remove_task_warn = True
        new_remove_res_warn = True
        new_timeline_colours = [(169, 169, 169), (255, 69, 69), (255, 165, 0), (50, 205, 50)]
        new_height = 600
        new_width = 800
        new_start_maximized = True

        self.project.update_settings(new_title, new_description, new_timeline_colours, new_height, new_width, new_remove_task_warn, new_remove_res_warn, new_start_maximized)

        # Reset the UI elements
        self.task_delete_warning.setChecked(self.project.settings.remove_task_warn)
        self.res_delete_warning.setChecked(self.project.settings.remove_res_warn)
        self.start_max.setChecked(self.project.settings.start_maximized)

        self.height_edit.setText(str(self.project.settings.default_height))
        self.width_edit.setText(str(self.project.settings.default_width))

        QMessageBox.information(
            self, 
            "Settings Updated", 
            "Some settings may require you to reload the project to take effect.", 
            QMessageBox.Ok
        )


    # If height is empty or 0, set it to 1
    def verify_height(self):
        if not self.height_edit.text() or int(self.height_edit.text()) == 0:
            self.height_edit.setText('1')

    # If width is empty or 0, set it to 1
    def verify_width(self):
        if not self.width_edit.text() or int(self.width_edit.text()) == 0:
            self.width_edit.setText('1')

    # Updates the settings
    def update_settings(self):
        self.verify_height()
        self.verify_width()

        new_title = self.project_title.text()
        new_description = self.project_description.toPlainText()
        new_remove_task_warn = self.task_delete_warning.isChecked()
        new_remove_res_warn = self.res_delete_warning.isChecked()
        new_timeline_colours = self.project.settings.timeline_colours
        new_height = int(self.height_edit.text())
        new_width = int(self.width_edit.text())
        new_start_maximized = self.start_max.isChecked()

        self.project.update_settings(new_title, new_description, new_timeline_colours, new_height, new_width, new_remove_task_warn, new_remove_res_warn, new_start_maximized)
        
        QMessageBox.information(
            self, 
            "Settings Updated", 
            "Some settings may require you to reload the project to take effect.", 
            QMessageBox.Ok
        )
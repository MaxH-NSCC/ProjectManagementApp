from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit, QCheckBox, QPushButton

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

        layout.addRow("Project Title:", self.project_title)
        layout.addRow("Project Description:", self.project_description)
        layout.addWidget(self.task_delete_warning)
        layout.addWidget(self.res_delete_warning)
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

        self.project.update_settings(new_title, new_description, new_timeline_colours, new_height, new_width, new_remove_task_warn, new_remove_res_warn)

    # Updates the settings
    def update_settings(self):
        new_title = self.project_title.text()
        new_description = self.project_description.toPlainText()
        new_remove_task_warn = self.task_delete_warning.isChecked()
        new_remove_res_warn = self.res_delete_warning.isChecked()
        new_timeline_colours = self.project.settings.timeline_colours
        new_height = self.project.settings.default_height
        new_width = self.project.settings.default_width

        self.project.update_settings(new_title, new_description, new_timeline_colours, new_height, new_width, new_remove_task_warn, new_remove_res_warn)
        
        # Colour picks for timeline colours
        # Number inputs for the default width and height
        # Checkbox for task deletion warning
        # Checkbox for res deletion warning
        # Reset settings to default option that gives warning
        # Save settings button that says you may need to restart the app to see some changes (Saves settings, updates task title and description)
        # make it say it wont update the project files filename so you'll need to change that yourself if you want that

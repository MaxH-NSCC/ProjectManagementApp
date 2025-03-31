from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit, QCheckBox

class ProjectOptionsTab(QWidget):
    def __init__(self, project, parent=None):
        super().__init__(parent)
        self.project = project
        layout = QFormLayout()

        self.project_title = QLineEdit(self.project.title)
        self.project_description = QTextEdit(self.project.description)

        layout.addRow("Project Title:", self.project_title)
        layout.addRow("Project Description:", self.project_description)

        
        # Colour picks for timeline colours
        # Number inputs for the default width and height
        # Checkbox for task deletion warning
        # Checkbox for res deletion warning
        # Reset settings to default option that gives warning
        # Save settings button that says you may need to restart the app to see some changes (Saves settings, updates task title and description)
        # make it say it wont update the project files filename so you'll need to change that yourself if you want that



        self.setLayout(layout)

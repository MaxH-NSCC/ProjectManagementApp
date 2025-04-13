from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QDateEdit, QMessageBox
from PyQt5.QtCore import QDate

class TaskDialog(QDialog):
    def __init__(self, title="", description="", start_date=None, end_date=None, read_only=False, project=None, parent=None):
        super().__init__(parent)
        self.project = project
        self.original_title = title
        self.setWindowTitle("Task Details" if read_only else "Edit/Create Task")
        self.resize(400, 400)
        layout = QVBoxLayout()

        self.title_edit = QLineEdit(title)
        self.desc_edit = QTextEdit(description)

        if read_only:
            self.title_edit.setReadOnly(True)
            self.desc_edit.setReadOnly(True)

        # Date selection widgets
        self.start_date_edit = QDateEdit()
        self.end_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.end_date_edit.setCalendarPopup(True)

        # Default to today if no date is provided
        today = QDate.currentDate()

        # Ensure dates are passed as strings in the "yyyy-MM-dd" format
        if start_date:
            self.start_date_edit.setDate(QDate.fromString(start_date, "yyyy-MM-dd"))
        else:
            self.start_date_edit.setDate(today)

        if end_date:
            self.end_date_edit.setDate(QDate.fromString(end_date, "yyyy-MM-dd"))
        else:
            self.end_date_edit.setDate(today)

        if read_only:
            self.start_date_edit.setEnabled(False)
            self.end_date_edit.setEnabled(False)

        layout.addWidget(QLabel("Title:"))
        layout.addWidget(self.title_edit)
        layout.addWidget(QLabel("Description:"))
        layout.addWidget(self.desc_edit)
        layout.addWidget(QLabel("Start Date:"))
        layout.addWidget(self.start_date_edit)
        layout.addWidget(QLabel("End Date:"))
        layout.addWidget(self.end_date_edit)

        if not read_only:
            self.ok_button = QPushButton("Save")
            self.ok_button.clicked.connect(self.validate_and_accept) # self.accept will do it without validation
            layout.addWidget(self.ok_button)

        self.setLayout(layout)

    def validate_and_accept(self):
        title = self.title_edit.text().strip()
        if not title:
            QMessageBox.warning(self, "Invalid Input", "Task title cannot be empty!")
            return
        # Check if editing an existing task
        existing_task = self.project.get_task_by_title(self.original_title) if self.project else None
        # Prevent duplicates only if changing to a new title
        if self.project and self.project.task_exists(title) and (existing_task is None or existing_task.title != title):
            QMessageBox.warning(self, "Duplicate Task", "A task with this name already exists!")
            return
        self.accept()

    def get_task_details(self):
        return (
            self.title_edit.text(),
            self.desc_edit.toPlainText(),
            self.start_date_edit.date().toString("yyyy-MM-dd"),
            self.end_date_edit.date().toString("yyyy-MM-dd"),
        )

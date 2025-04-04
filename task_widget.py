from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit

# Custom part of the UI used to display more information in the task view UI
class TaskWidget(QWidget):
    def __init__(self, title, description, start_date=None, end_date=None, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout()
        self.maxTextLength = 60
        self.description = description
        self.description_text = description[:self.maxTextLength] + " ..." if len(description) > self.maxTextLength else description

        self.title_label = QLabel(title)
        self.desc_label = QLabel(self.description_text)

        self.start_date_label = QLabel(f"Start Date: {start_date if start_date else 'N/A'}")
        self.end_date_label = QLabel(f"End Date: {end_date if end_date else 'N/A'}")

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.desc_label)
        self.layout.addWidget(self.start_date_label)
        self.layout.addWidget(self.end_date_label)

        self.setLayout(self.layout)

    # Getter for details
    def get_details(self):
        start_date_text = self.start_date_label.text().replace("Start Date: ", "").strip()
        end_date_text = self.end_date_label.text().replace("End Date: ", "").strip()
        return self.title_label.text(), self.description, start_date_text, end_date_text

    # Setter for details
    def set_details(self, title, description, start_date=None, end_date=None):
        self.title_label.setText(title)
        self.desc_label.setText(self.description_text)
        self.start_date_label.setText(f"Start Date: {start_date if start_date else 'N/A'}")
        self.end_date_label.setText(f"End Date: {end_date if end_date else 'N/A'}")
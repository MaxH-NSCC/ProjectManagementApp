from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class TaskWidget(QWidget):
    def __init__(self, title, description, start_date=None, end_date=None, parent=None):
        super().__init__(parent)

        self.maxTextLength = 60
        self.description = description
        self.description_text = description[:self.maxTextLength] + " ..." if len(description) > self.maxTextLength else description

        # Main layout with padding
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(5, 5, 5, 5)

        # Main frame
        frame = QFrame()
        frame.setObjectName("taskFrame")
        frame_layout = QVBoxLayout(frame)
        frame_layout.setSpacing(4)

        # Title
        self.title_label = QLabel(title)
        self.title_label.setFont(QFont("Segoe UI", 10))
        frame_layout.addWidget(self.title_label)

        # Description Frame
        desc_frame = QFrame()
        desc_frame.setObjectName("descFrame")
        desc_layout = QVBoxLayout(desc_frame)

        # Description
        self.desc_label = QLabel(self.description_text)
        self.desc_label.setWordWrap(True)
        desc_layout.addWidget(self.desc_label)
        frame_layout.addWidget(desc_frame)

        # Dates Frame
        dates_frame = QFrame()
        dates_frame.setObjectName("datesFrame")
        dates_layout = QHBoxLayout(dates_frame)

        # Dates
        self.start_date_label = QLabel(f"Start Date: {start_date if start_date else 'N/A'}")
        self.end_date_label = QLabel(f"End Date: {end_date if end_date else 'N/A'}")
        dates_layout.addWidget(self.start_date_label)
        dates_layout.addWidget(self.end_date_label)
        frame_layout.addWidget(dates_frame)

        outer_layout.addWidget(frame)



    def get_details(self):
        start_date_text = self.start_date_label.text().replace("Start Date: ", "").strip()
        end_date_text = self.end_date_label.text().replace("End Date: ", "").strip()
        return self.title_label.text(), self.description, start_date_text, end_date_text

    def set_details(self, title, description, start_date=None, end_date=None):
        self.title_label.setText(title)
        self.description = description
        self.description_text = description[:self.maxTextLength] + " ..." if len(description) > self.maxTextLength else description
        self.desc_label.setText(self.description_text)
        self.start_date_label.setText(f"Start Date: {start_date if start_date else 'N/A'}")
        self.end_date_label.setText(f"End Date: {end_date if end_date else 'N/A'}")

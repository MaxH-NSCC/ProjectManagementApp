from PyQt5.QtWidgets import QWidget, QTableView, QHBoxLayout
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, QAbstractTableModel
from datetime import datetime, timedelta
from task_dialog import TaskDialog

class GanttModel(QAbstractTableModel):
    def __init__(self, project):
        super().__init__()
        self.project = project
        self.tasks = project.tasks
        self.settings = project.settings
        self.start_date, self.end_date = self.get_time_range()
        
        self.STATUS_COLORS = {
            "Backlog": QColor(*self.project.settings.timeline_colours[0]),
            "To Do": QColor(*self.project.settings.timeline_colours[1]),
            "Doing": QColor(*self.project.settings.timeline_colours[2]),
            "Done": QColor(*self.project.settings.timeline_colours[3])
        }

    def get_time_range(self):
        self.beginResetModel()
        if not self.tasks:
            today = datetime.today()
            self.start_date, self.end_date = today, today
        else:
            # Find the earliest start date and latest end date across all tasks
            self.start_date = min(datetime.strptime(task.start_date, "%Y-%m-%d") for task in self.tasks)
            self.end_date = max(datetime.strptime(task.end_date, "%Y-%m-%d") for task in self.tasks)
        self.endResetModel()
        return self.start_date, self.end_date

    def rowCount(self, parent=None):
        return len(self.tasks)

    def columnCount(self, parent=None):
        return (self.end_date - self.start_date).days + 1  

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        
        row, col = index.row(), index.column()
        task = self.tasks[row]
        task_start = (datetime.strptime(task.start_date, "%Y-%m-%d") - self.start_date).days
        task_end = (datetime.strptime(task.end_date, "%Y-%m-%d") - self.start_date).days

        if role == Qt.DisplayRole:
            return ""

        if role == Qt.BackgroundRole:
            if task_start <= col <= task_end:
                return self.STATUS_COLORS.get(task.category, QColor(100, 150, 255))

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return (self.start_date + timedelta(days=section)).strftime("%Y-%m-%d")
            elif orientation == Qt.Vertical:
                return self.tasks[section].title
        return None

    def updateModel(self):
        self.beginResetModel()
        self.tasks = self.project.tasks
        self.start_date, self.end_date = self.get_time_range()
        self.endResetModel()

class TimelineTab(QWidget):
    def __init__(self, project, parent=None):
        super().__init__(parent)
        self.project = project
        layout = QHBoxLayout()

        self.timeline_table = QTableView()
        
        self.timeline_model = GanttModel(self.project)
        self.timeline_table.setModel(self.timeline_model)

        self.timeline_table.horizontalHeader().setDefaultSectionSize(100)
        self.timeline_table.verticalHeader().setDefaultSectionSize(30)
        self.timeline_table.setHorizontalScrollMode(QTableView.ScrollPerPixel)
        self.timeline_table.setVerticalScrollMode(QTableView.ScrollPerPixel)
        self.timeline_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.timeline_table.setSelectionMode(QTableView.SingleSelection)
        
        self.timeline_table.verticalHeader().sectionDoubleClicked.connect(self.view_task)
                    
        layout.addWidget(self.timeline_table)
        self.setLayout(layout)

    def refresh(self):
        self.timeline_model.updateModel()
        self.timeline_table.viewport().update()

    def view_task(self, row_index):
        task = self.timeline_model.tasks[row_index]  # Get the task by row index
        dialog = TaskDialog(task.title, task.description, task.start_date, task.end_date, read_only=True, project=self.project)
        dialog.exec_()

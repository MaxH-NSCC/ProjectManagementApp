from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QLabel, QPushButton, QMenu, QAction, QListWidgetItem, QMessageBox
from PyQt5.QtCore import Qt
from task_widget import TaskWidget
from task_dialog import TaskDialog
from core import *

class TaskTab(QWidget):
    def __init__(self, project, parent=None):
        super().__init__(parent)
        self.project = project
        self.layout = QVBoxLayout()

        # Task columns for UI
        self.task_layout = QHBoxLayout()
        self.columns = {
            "Backlog": QListWidget(),
            "To Do": QListWidget(),
            "Doing": QListWidget(),
            "Done": QListWidget()
        }

        # Setting up columns
        for col_name, widget in self.columns.items():
            column_layout = QVBoxLayout()
            column_layout.addWidget(QLabel(col_name))
            widget.setContextMenuPolicy(Qt.CustomContextMenu)
            widget.customContextMenuRequested.connect(self.show_context_menu)
            widget.itemDoubleClicked.connect(self.view_task)
            column_layout.addWidget(widget)
            self.task_layout.addLayout(column_layout)

        self.layout.addLayout(self.task_layout)

        self.add_task_btn = QPushButton("Add Task")
        self.add_task_btn.clicked.connect(self.create_task)
        self.layout.addWidget(self.add_task_btn)

        self.setLayout(self.layout)
        self.refresh_ui()

    def refresh_ui(self):
        for column in self.columns.values():
            column.clear()
        for task in self.project.get_tasks():
            self.add_task_to_ui(task)

    def add_task_to_ui(self, task):
        task_item = QListWidgetItem()
        task_widget = TaskWidget(task.title, task.description, task.start_date, task.end_date)
        task_item.setSizeHint(task_widget.sizeHint())
        self.columns[task.category].addItem(task_item)
        self.columns[task.category].setItemWidget(task_item, task_widget)

    def create_task(self):
        dialog = TaskDialog(project=self.project)
        if dialog.exec_():
            title, desc, start_date, end_date = dialog.get_task_details()
            if title:
                if self.project.task_exists(title):
                    QMessageBox.warning(self, "Duplicate Task", "A task with this name already exists!")
                    return
                task = Task(title, desc, start_date=start_date, end_date=end_date)
                if self.project.add_task(task):
                    self.refresh_ui()
                else:
                    QMessageBox.warning(self, "Error", "Failed to add task!")

    def move_task(self, item, from_widget, to_column):
        task_widget = from_widget.itemWidget(item)
        if task_widget:
            title, _, _, _ = task_widget.get_details()
            if self.project.update_task_category(title, to_column):
                self.refresh_ui()

    def view_task(self, item):
        for col in self.columns.values():
            if col.indexFromItem(item).isValid():
                task_widget = col.itemWidget(item)
                if task_widget:
                    title, desc, start_date, end_date = task_widget.get_details()
                    dialog = TaskDialog(title, desc, start_date, end_date, read_only=True, project=self.project)
                    dialog.exec_()
                break

    def show_context_menu(self, position):
        sender_widget = self.sender()
        item = sender_widget.itemAt(position)
        if item:
            menu = QMenu()
            edit_action = QAction("Edit", self)
            remove_action = QAction("Remove", self)
            move_action = QMenu("Move to")

            for col in self.columns:
                if self.columns[col] != sender_widget:
                    move_action.addAction(col, lambda col=col: self.move_task(item, sender_widget, col))

            edit_action.triggered.connect(lambda: self.edit_task(item))
            remove_action.triggered.connect(lambda: self.remove_task(item, sender_widget))

            menu.addAction(edit_action)
            menu.addMenu(move_action)
            menu.addAction(remove_action)
            menu.exec_(sender_widget.mapToGlobal(position))

    def edit_task(self, item):
        for col in self.columns.values():
            if col.indexFromItem(item).isValid():
                task_widget = col.itemWidget(item)
                if task_widget:
                    old_title, old_desc, old_start_date, old_end_date = task_widget.get_details()
                    task = self.project.get_task_by_title(old_title)

                    if task:
                        dialog = TaskDialog(old_title, old_desc, start_date=old_start_date, end_date=old_end_date, project=self.project)
                        if dialog.exec_():
                            new_title, new_desc, new_start_date, new_end_date = dialog.get_task_details()
                            if old_title != new_title and self.project.task_exists(new_title):
                                QMessageBox.warning(self, "Duplicate Task", "A task with this name already exists!")
                                return
                            if self.project.update_task_details(old_title, new_title, new_desc, new_start_date, new_end_date):
                                self.refresh_ui()
                    break

    def remove_task(self, item, widget):
        task_widget = widget.itemWidget(item)
        if not task_widget:
            return
        title, _, _, _ = task_widget.get_details()

        if self.project.settings.remove_task_warn:
            reply = QMessageBox.question(
                widget,
                "Confirm Task Deletion",
                f"Are you sure you want to remove the task '{title}'?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.No:
                return

        self.project.remove_task(title)
        self.refresh_ui()
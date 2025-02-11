import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTabWidget, QListWidget, QListWidgetItem, QMenu, QAction, QDialog, QLabel, QTextEdit, QLineEdit, QHBoxLayout, QMessageBox, QFormLayout
from PyQt5.QtCore import Qt

class TaskDialog(QDialog):
    def __init__(self, title="", description="", read_only=False, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Task Details" if read_only else "New Task")
        layout = QVBoxLayout()
        
        self.title_edit = QLineEdit(title)
        self.desc_edit = QTextEdit(description)
        
        if read_only:
            self.title_edit.setReadOnly(True)
            self.desc_edit.setReadOnly(True)
        
        layout.addWidget(QLabel("Title:"))
        layout.addWidget(self.title_edit)
        layout.addWidget(QLabel("Description:"))
        layout.addWidget(self.desc_edit)
        
        if not read_only:
            self.ok_button = QPushButton("Save")
            self.ok_button.clicked.connect(self.accept)
            layout.addWidget(self.ok_button)
        
        self.setLayout(layout)
    
    def get_task_details(self):
        return self.title_edit.text(), self.desc_edit.toPlainText()

class ProjectScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Project Management App")
        self.resize(800, 600)
        
        layout = QVBoxLayout()
        self.tabs = QTabWidget()
        
        self.task_board = QWidget()
        self.task_layout = QHBoxLayout()
        
        self.columns = {
            "To Do": QListWidget(),
            "Doing": QListWidget(),
            "Done": QListWidget()
        }
        
        for col_name, widget in self.columns.items():
            column_layout = QVBoxLayout()
            column_layout.addWidget(QLabel(col_name))
            widget.setContextMenuPolicy(Qt.CustomContextMenu)
            widget.customContextMenuRequested.connect(self.show_context_menu)
            widget.itemDoubleClicked.connect(self.view_task)
            column_layout.addWidget(widget)
            self.task_layout.addLayout(column_layout)
        
        self.task_board.setLayout(self.task_layout)
        
        self.project_options = QWidget()
        project_layout = QFormLayout()
        self.project_title = QLineEdit()
        self.project_description = QTextEdit()
        project_layout.addRow("Project Title:", self.project_title)
        project_layout.addRow("Project Description:", self.project_description)
        self.project_options.setLayout(project_layout)
        
        self.tabs.addTab(self.task_board, "Tasks")
        self.tabs.addTab(QWidget(), "Resources")
        self.tabs.addTab(QWidget(), "Timeline")
        self.tabs.addTab(self.project_options, "Project Options")
        
        layout.addWidget(self.tabs)
        
        self.add_task_btn = QPushButton("Add Task")
        self.add_task_btn.clicked.connect(self.create_task)
        
        layout.addWidget(self.add_task_btn)
        self.setLayout(layout)
    
    def create_task(self):
        dialog = TaskDialog()
        if dialog.exec_():
            title, desc = dialog.get_task_details()
            if title:
                item = QListWidgetItem(title)
                item.setData(Qt.UserRole, desc)
                self.columns["To Do"].addItem(item)
    
    def view_task(self, item):
        dialog = TaskDialog(item.text(), item.data(Qt.UserRole), read_only=True)
        dialog.exec_()
    
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
        dialog = TaskDialog(item.text(), item.data(Qt.UserRole))
        if dialog.exec_():
            title, desc = dialog.get_task_details()
            item.setText(title)
            item.setData(Qt.UserRole, desc)
    
    def remove_task(self, item, widget):
        widget.takeItem(widget.row(item))
    
    def move_task(self, item, from_widget, to_column):
        new_item = QListWidgetItem(item.text())
        new_item.setData(Qt.UserRole, item.data(Qt.UserRole))
        self.columns[to_column].addItem(new_item)
        from_widget.takeItem(from_widget.row(item))
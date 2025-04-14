import os
import json
import webbrowser
import core
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget, QMenuBar, QMenu, QAction, QFileDialog, QMessageBox
from PyQt5.QtGui import QKeySequence
from core import *
from task_tab import TaskTab
from resources_tab import ResourcesTab
from timeline_tab import TimelineTab
from project_options_tab import ProjectOptionsTab

class ProjectScreen(QWidget):
    def __init__(self, project, file_path=None):
        super().__init__()
        self.project = project
        self.current_file = file_path
        self.prevent_close_event = False
        self.setWindowTitle(f"Project: {project.title}")
        self.resize(self.project.settings.default_width, self.project.settings.default_height)

        layout = QVBoxLayout()
        self.menu_bar = QMenuBar()
        
        # File menu
        file_menu = QMenu("File", self)

        # Load Project action (Ctrl + O)
        load_action = QAction("Open Project", self)
        load_action.setShortcut(QKeySequence("Ctrl+O"))  # Set shortcut
        load_action.triggered.connect(self.load_project)

        # Save action (Ctrl + S)
        save_action = QAction("Save", self)
        save_action.setShortcut(QKeySequence("Ctrl+S"))  # Set shortcut
        save_action.triggered.connect(self.save_project)

        # Save As action (Ctrl + Shift + S)
        save_as_action = QAction("Save As", self)
        save_as_action.setShortcut(QKeySequence("Ctrl+Shift+S"))  # Set shortcut
        save_as_action.triggered.connect(self.save_project_as)

        file_menu.addAction(load_action)
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)
        self.menu_bar.addMenu(file_menu)

        # Add App Settings Menu
        app_settings_menu = QMenu("App Settings", self)

        # Light Theme action
        light_theme_action = QAction("Light Theme", self)
        light_theme_action.triggered.connect(lambda: self.set_theme("light"))

        # Dark Theme action
        dark_theme_action = QAction("Dark Theme", self)
        dark_theme_action.triggered.connect(lambda: self.set_theme("dark"))

        # Add actions to the App Settings menu
        app_settings_menu.addAction(light_theme_action)
        app_settings_menu.addAction(dark_theme_action)

        self.menu_bar.addMenu(app_settings_menu)

        # Add Help Menu
        help_menu = QMenu("Help", self)

        # Help Action (opens help.txt file)
        help_action = QAction("View Help", self)
        help_action.triggered.connect(self.open_help_file)

        # GitHub Link Action
        github_action = QAction("View GitHub", self)
        github_action.triggered.connect(self.open_github)

        help_menu.addAction(help_action)
        help_menu.addAction(github_action)

        self.menu_bar.addMenu(help_menu)


        layout.setMenuBar(self.menu_bar)

        self.tabs = QTabWidget()
        
        # Create tabs
        self.task_tab = TaskTab(self.project)
        self.resources_tab = ResourcesTab(self.project)
        self.timeline_tab = TimelineTab(self.project)
        self.options_tab = ProjectOptionsTab(self.project)
        
        # Add tabs
        self.tabs.addTab(self.task_tab, "Tasks")
        self.tabs.addTab(self.resources_tab, "Resources")
        self.tabs.addTab(self.timeline_tab, "Timeline")
        self.tabs.addTab(self.options_tab, "Project Options")
        
        self.tabs.currentChanged.connect(self.on_tab_changed)
        
        layout.addWidget(self.tabs)
        self.setLayout(layout)

        if project.settings.start_maximized:
            self.showMaximized()

    def on_tab_changed(self, index):
        if self.tabs.tabText(index) == "Timeline":
            self.timeline_tab.refresh()

    def save_project(self):
        if core.loaded:  # If loaded is True, just save
            self._write_to_file(self.current_file)
        else:  # Otherwise, do "Save As"
            self.save_project_as()

    def save_project_as(self):
        options = QFileDialog.Options()
        
        # Default to Projects directory inside app directory
        app_dir = os.path.dirname(os.path.abspath(__file__))
        default_path = os.path.join(app_dir, "Projects")

        # Suggest project name as default file name
        suggested_name = os.path.join(default_path, f"{self.project.title}.json")
        
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Project As", suggested_name, "JSON Files (*.json)", options=options)
        
        if file_name:
            self.current_file = file_name
            core.loaded = True
            self._write_to_file(file_name)

    def _write_to_file(self, file_path):
        try:
            data = {
                "Project Management App Json File": True,
                "project": self.project.to_dict()
            }
            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)
            
            QMessageBox.information(self, "Save Successful", "Project saved successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Failed to save project: {e}")

    def load_project(self):
        reply = QMessageBox.question(
            self, "Load Project", "Do you want to save changes before loading another project?",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
        )

        if reply == QMessageBox.Cancel:
            return  

        if reply == QMessageBox.Yes:
            self.save_project()  

        # Prevent closeEvent from asking again
        self.prevent_close_event = True  
        
        from ui_main import StartupScreen
        self.startup_screen = StartupScreen()
        self.startup_screen.show()
        
        self.close()

    def closeEvent(self, event):
            if self.prevent_close_event:
                event.accept()  # Bypass confirmation when prevent_close_event is True
                return  

            # Normal close confirmation
            reply = QMessageBox.question(
                self, "Exit", "Do you want to save changes before exiting?",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
            )

            if reply == QMessageBox.Cancel:
                event.ignore()  # Stop the window from closing
            elif reply == QMessageBox.Yes:
                self.save_project()
                event.accept()
            else:
                event.accept()

    def open_help_file(self):
        help_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'help.txt')
        if os.path.exists(help_file_path):
            os.startfile(help_file_path)

    def open_github(self):
        webbrowser.open("https://github.com/MaxH-NSCC/ProjectManagementApp")

    def set_theme(self, theme):
        from core import save_app_settings, AppSettings
        save_app_settings(AppSettings(theme=theme))
        path = "style.qss" if theme == "light" else "style_dark.qss"
        try:
            with open(path, "r") as f:
                self.setStyleSheet(f.read())
                QApplication.instance().setStyleSheet(f.read())  # Apply to the whole app
        except FileNotFoundError:
            print(f"{path} not found. Skipping stylesheet.")
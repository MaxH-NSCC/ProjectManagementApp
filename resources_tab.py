import os
import webbrowser
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem, QDialog, QLineEdit, QFileDialog, QHBoxLayout, QLabel, QMessageBox, QMenu, QApplication, QCheckBox
from PyQt5.QtCore import Qt
from core import *

class ResourcesTab(QWidget):
    def __init__(self, project, parent=None):
        super().__init__(parent)
        self.project = project  # store reference to the project
        self.layout = QVBoxLayout()


        # filters
        filter_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search by name...")
        self.search_bar.textChanged.connect(self.apply_filters)

        self.file_checkbox = QCheckBox("Files")
        self.file_checkbox.setChecked(True)
        self.file_checkbox.stateChanged.connect(self.apply_filters)

        self.link_checkbox = QCheckBox("Links")
        self.link_checkbox.setChecked(True)
        self.link_checkbox.stateChanged.connect(self.apply_filters)

        filter_layout.addWidget(QLabel("Filter:"))
        filter_layout.addWidget(self.search_bar)
        filter_layout.addWidget(self.file_checkbox)
        filter_layout.addWidget(self.link_checkbox)
        self.layout.addLayout(filter_layout)

        # resource list
        self.resource_list = QListWidget()
        self.resource_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.resource_list.customContextMenuRequested.connect(self.show_context_menu)
        self.layout.addWidget(self.resource_list)

        # buttons for adding a resource
        self.add_file_button = QPushButton("Add File Resource")
        self.add_link_button = QPushButton("Add Web Link")

        self.add_file_button.clicked.connect(self.add_file_resource)
        self.add_link_button.clicked.connect(self.add_link_resource)

        self.layout.addWidget(self.add_file_button)
        self.layout.addWidget(self.add_link_button)

        self.setLayout(self.layout)

        self.refresh_list()  # load existing resources


    def apply_filters(self):
        query = self.search_bar.text().lower()
        show_files = self.file_checkbox.isChecked()
        show_links = self.link_checkbox.isChecked()

        filtered = []
        for res in self.project.resources:
            name_matches = query in res.title.lower()
            type_matches = (res.is_link and show_links) or (not res.is_link and show_files)

            if name_matches and type_matches:
                filtered.append(res)

        self.refresh_list(filtered)

    def refresh_list(self, filtered_resources=None):
        self.resource_list.clear()

        resources_to_display = filtered_resources if filtered_resources is not None else self.project.resources
        sorted_resources = sorted(resources_to_display, key=lambda r: r.title.lower())

        for res in sorted_resources:
            item = QListWidgetItem(f"{res.title} ({'Link' if res.is_link else 'File'})")
            item.setData(Qt.UserRole, res)
            self.resource_list.addItem(item)

    def add_file_resource(self):
        # prompt user to select a file and add it as a resource
        app_settings = load_app_settings()
        initial_dir = app_settings.last_resource_dir or os.path.expanduser("~")
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", initial_dir)
        if file_path:

            # Save last directory as default
            app_settings.last_resource_dir = os.path.dirname(file_path)
            save_app_settings(app_settings)

            title = os.path.basename(file_path)
            resource = Resource(title, file_path, is_link=False)
            if self.project.add_resource(resource):
                self.apply_filters()
            else:
                QMessageBox.warning(self, "Duplicate Resource", "A resource with this name already exists!")


    def add_link_resource(self):
        dialog = ResourceDialog()
        if dialog.exec_():
            title, link = dialog.get_details()
            if title and link:
                resource = Resource(title, link, is_link=True)
                if self.project.add_resource(resource):
                    self.apply_filters()
                else:
                    QMessageBox.warning(self, "Duplicate Resource", "A resource with this name already exists!")

    def open_selected_resource(self, item):
        # open the selected resource (file or link)
        resource = item.data(Qt.UserRole)
        if resource.is_link:
            webbrowser.open(resource.path)  # Open web link in browser
        else:
            os.startfile(resource.path)  # Open file with default program

    def show_context_menu(self, position):
        # display right-click context menu based on the selected resource
        item = self.resource_list.itemAt(position)
        if not item:
            return

        resource = item.data(Qt.UserRole)
        menu = QMenu(self)

        open_action = menu.addAction("Open")
        copy_action = menu.addAction("Copy URL" if resource.is_link else "Copy Path")
        remove_action = menu.addAction("Remove")

        action = menu.exec_(self.resource_list.viewport().mapToGlobal(position))

        if action == open_action:
            self.open_resource(resource)
        elif action == copy_action:
            self.copy_to_clipboard(resource.path)
        elif action == remove_action:
            self.remove_resource(resource)

    def open_resource(self, resource):
        # open file or URL
        if resource.is_link:
            webbrowser.open(resource.path)  # Open web link
        else:
            os.startfile(resource.path)  # Open file with default program

    def copy_to_clipboard(self, text):
        # copy text to clipboard
        clipboard = QApplication.clipboard()
        clipboard.setText(text)

    def remove_resource(self, resource):
        # remove resource from project
        if self.project.settings.remove_res_warn:
            reply = QMessageBox.question(
                self,
                "Confirm Task Deletion",
                f"Are you sure you want to remove the task '{resource.title}'?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.No:
                return  # User canceled, do nothing
            
        self.project.remove_resource(resource.title)
        self.refresh_list()
        

class ResourceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Web Link")
        self.layout = QVBoxLayout()

        self.title_edit = QLineEdit()
        self.link_edit = QLineEdit()

        self.layout.addWidget(QLabel("Title:"))
        self.layout.addWidget(self.title_edit)
        self.layout.addWidget(QLabel("Web Link:"))
        self.layout.addWidget(self.link_edit)

        self.ok_button = QPushButton("Add")
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)

        self.setLayout(self.layout)

    def get_details(self):
        return self.title_edit.text().strip(), self.link_edit.text().strip()
from datetime import datetime
import json
import os

loaded = False

class Task:
    def __init__(self, title, description, category="Backlog", start_date=None, end_date=None):
        self.title = title
        self.description = description
        self.category = category
        # Default to today if no start_date or end_date is passed
        self.start_date = start_date or datetime.today().strftime("%Y-%m-%d")  # Default to today if None
        self.end_date = end_date or self.start_date  # Default end_date to start_date if not provided

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "start_date": self.start_date,
            "end_date": self.end_date,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["title"],
            data["description"],
            data["category"],
            data.get("start_date"),
            data.get("end_date"),
        )
    
class Settings:
    def __init__(self, timeline_colours=None, tabs_displayed=None, default_height=600, default_width=800, remove_task_warn=None, remove_res_warn=None):
        self.timeline_colours = timeline_colours or [(169, 169, 169), (255, 69, 69), (255, 165, 0), (50, 205, 50)]
        self.tabs_displayed = tabs_displayed or [True, True, True]
        self.default_height = default_height
        self.default_width = default_width
        self.remove_task_warn = remove_task_warn if remove_task_warn is not None else True
        self.remove_res_warn = remove_res_warn if remove_res_warn is not None else True

    def to_dict(self):
        return {
            "timeline_colours": self.timeline_colours,
            "tabs_displayed": self.tabs_displayed,
            "default_height": self.default_height,
            "default_width": self.default_width,
            "remove_task_warn": self.remove_task_warn,
            "remove_res_warn": self.remove_res_warn,
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get("timeline_colours"),
            data.get("tabs_displayed"),
            data.get("default_height", 600),
            data.get("default_width", 800),
            data.get("remove_task_warn"),
            data.get("remove_res_warn"),
        )
    

class Resource:
    def __init__(self, title, path, is_link=False):
        self.title = title
        self.path = path  # file path or URL
        self.is_link = is_link  # true if it's a web link, False if it's a file

    def to_dict(self):
        return {"title": self.title, "path": self.path, "is_link": self.is_link}

    @classmethod
    def from_dict(cls, data):
        return cls(data["title"], data["path"], data["is_link"])
    

class Project:
    # project contains tasks
    def __init__(self, title, description, settings=None):
        self.title = title
        self.description = description
        self.tasks = []
        self.resources = []
        self.settings = settings or Settings()

    def task_exists(self, title):
        return any(task.title == title for task in self.tasks)

    def add_task(self, task):
        if self.task_exists(task.title):
            return False
        self.tasks.append(task)
        return True

    def remove_task(self, title):
        for i in range(len(self.tasks)):
            if self.tasks[i].title == title:
                del self.tasks[i]
                break

    def update_task_category(self, title, new_category):
        for task in self.tasks:
            if task.title == title:
                task.category = new_category
                return True
        return False

    def update_task_details(self, old_title, new_title, new_description, new_start, new_end):
        if old_title != new_title and self.task_exists(new_title):
            return False
        
        for task in self.tasks:
            if task.title == old_title:
                task.title = new_title
                task.description = new_description
                task.start_date = new_start
                task.end_date = new_end
                return True
        return False
    
    def get_task_by_title(self, title):
        return next((task for task in self.tasks if task.title == title), None)
    
    def get_tasks(self):
        return self.tasks 
    
    def add_resource(self, resource):
        if any(r.title == resource.title for r in self.resources):  # Prevent duplicate names
            return False
        self.resources.append(resource)
        return True

    def remove_resource(self, title):
        for i in range(len(self.resources)):
            if self.resources[i].title == title:
                del self.resources[i]
                break

    def update_settings(self, new_timeline_colours, new_tabs_displayed, new_height, new_width, new_remove_task_warn, new_remove_res_warn):
        self.settings.timeline_colours = new_timeline_colours
        self.settings.tabs_displayed = new_tabs_displayed
        self.settings.default_height = new_height
        self.settings.default_width = new_width
        self.remove_task_warn = new_remove_task_warn
        self.remove_res_warn = new_remove_res_warn

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "tasks": [task.to_dict() for task in self.tasks],
            "resources": [res.to_dict() for res in self.resources],
            "settings": self.settings.to_dict(),
        }

    @classmethod
    def from_dict(cls, data):
        project = cls(data["title"], data["description"], Settings.from_dict(data.get("settings", {})))
        project.tasks = [Task.from_dict(task) for task in data["tasks"]]
        project.resources = [Resource.from_dict(res) for res in data.get("resources", [])]
        return project


class ProjectManager:
    # manages multiple projects
    def __init__(self):
        self.projects = []

    def create_project(self, title, description):
        project = Project(title, description, Settings())
        self.projects.append(project)
        return project

    def get_project(self, title):
        for project in self.projects:
            if project.title == title:
                return project
        return None

    def delete_project(self, title):
        self.projects = [project for project in self.projects if project.title != title]

def save_json(file_path, project):
    data = {
        "Project Management App Json File": True,  # Unique identifier
        "project": project.to_dict()
    }
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

def load_json(file_path):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)

            # Check for identifier
            if data.get("Project Management App Json File") is not True:
                print("Invalid JSON file: Missing project management identifier.")
                return None

            return Project.from_dict(data["project"])  # Load the single project

    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        print(f"Error loading JSON: {e}")
        return None  # Return None instead of a blank project
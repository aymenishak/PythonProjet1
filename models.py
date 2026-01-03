"""
Data models for User and Task objects.
These classes represent the data structure used throughout the application.
"""

import bcrypt
from datetime import datetime

class User:
    """Represents a user in the application with ID, username, and creation timestamp."""
    def __init__(self, user_id=None, username="", email=""):
        self.id = user_id
        self.username = username
        self.email = email
        self.created_at = datetime.now()

class Task:
    """Represents a task item with completion status and pomodoro tracking."""
    def __init__(self, task_id=None, title="", description=""):
        self.id = task_id
        self.user_id = None
        self.title = title
        self.description = description
        self.completed = False
        self.created_at = datetime.now()
        self.pomodoro_count = 0
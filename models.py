"""
Data structure definitions for User and Task.
These are simple data classes for reference only.
"""

class User:
    def __init__(self, user_id=None, username=""):
        self.id = user_id
        self.username = username

class Task:
    def __init__(self, task_id=None, title=""):
        self.id = task_id
        self.title = title
        self.completed = False
        self.pomodoro_count = 0

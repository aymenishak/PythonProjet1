"""
Database operations for storing users, tasks, and authentication data.
Uses SQLite for local storage and bcrypt for password security.
"""

import sqlite3
import bcrypt


class Database:
    """Handles all database operations including user management and task storage."""

    def __init__(self, db_name="pomodoro.db"):
        """Initialize database connection and create tables if they don't exist."""
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        """Create the users and tasks tables in the database."""
        cursor = self.conn.cursor()

        # Users table stores user credentials with hashed passwords
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')

        # Tasks table stores todo items linked to users
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                completed INTEGER DEFAULT 0,
                pomodoro_count INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')

        self.conn.commit()

    def add_user(self, username, password):
        """Register a new user with hashed password."""
        cursor = self.conn.cursor()
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        cursor.execute('''
            INSERT INTO users (username, password_hash)
            VALUES (?, ?)
        ''', (username, password_hash))
        self.conn.commit()
        return cursor.lastrowid

    def verify_user(self, username, password):
        """Authenticate user by checking username and password hash."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, password_hash FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode(), user[1]):
            return user
        return None

    def add_task(self, user_id, title):
        """Add a new task for a specific user."""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO tasks (user_id, title)
            VALUES (?, ?)
        ''', (user_id, title))
        self.conn.commit()
        return cursor.lastrowid

    def get_user_tasks(self, user_id):
        """Retrieve all tasks belonging to a specific user."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, title, completed, pomodoro_count FROM tasks WHERE user_id = ?', (user_id,))
        return cursor.fetchall()

    def complete_task(self, task_id):
        """Mark a task as completed."""
        cursor = self.conn.cursor()
        cursor.execute('UPDATE tasks SET completed = 1 WHERE id = ?', (task_id,))
        self.conn.commit()

    def delete_task(self, task_id):
        """Delete a task from the database."""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        self.conn.commit()

    def increment_pomodoro(self, task_id):
        """Increase the pomodoro count for a task."""
        cursor = self.conn.cursor()
        cursor.execute('UPDATE tasks SET pomodoro_count = pomodoro_count + 1 WHERE id = ?', (task_id,))
        self.conn.commit()
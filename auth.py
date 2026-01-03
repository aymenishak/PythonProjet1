"""
User authentication manager for login, registration, and session management.
Handles password validation and user session state.
"""

import sqlite3
from database import Database


class AuthManager:
    """Manages user authentication including login, registration, and logout."""

    def __init__(self):
        """Initialize authentication manager with database connection."""
        self.db = Database()
        self.current_user = None

    def register(self, username, password, confirm_password):
        """Register a new user with password confirmation and validation."""
        if password != confirm_password:
            return False, "Passwords do not match"

        if len(password) < 6:
            return False, "Password must be at least 6 characters"

        try:
            self.db.add_user(username, password)
            return True, "Registration successful!"
        except sqlite3.IntegrityError:
            return False, "Username already exists"

    def login(self, username, password):
        """Authenticate user and create session if credentials are valid."""
        user = self.db.verify_user(username, password)
        if user:
            self.current_user = {
                'id': user[0],
                'username': username
            }
            return True, "Login successful!"
        return False, "Invalid username or password"

    def logout(self):
        """End the current user session."""
        self.current_user = None
        return True, "Logged out successfully"

    def is_authenticated(self):
        """Check if a user is currently logged in."""
        return self.current_user is not None

    def get_current_user_id(self):
        """Get the ID of the currently logged in user."""
        return self.current_user['id'] if self.current_user else None
"""
Main GUI application built with CustomTkinter.
Provides login/registration screens, task management, and pomodoro timer interface.
"""

import customtkinter as ctk
from auth import AuthManager
from database import Database
from pomodoro_timer import PomodoroTimer


class PomodoroApp:
    """Main application class that manages all GUI screens and user interactions."""

    def __init__(self):
        """Initialize application with dark theme and default window size."""
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Pomodoro Todo App")
        self.root.geometry("700x500")

        self.auth = AuthManager()
        self.db = Database()
        self.timer = PomodoroTimer()

        self.show_login()

    def show_login(self):
        """Display login screen with username and password fields."""
        self.clear_window()

        frame = ctk.CTkFrame(self.root)
        frame.pack(expand=True, padx=40, pady=40)

        ctk.CTkLabel(frame, text="Pomodoro App", font=("Arial", 24, "bold")).pack(pady=20)

        self.username_entry = ctk.CTkEntry(frame, placeholder_text="Username")
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(frame, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10)

        ctk.CTkButton(frame, text="Login", command=self.login).pack(pady=10)
        ctk.CTkButton(frame, text="Register", command=self.show_register).pack(pady=5)

        self.auth_label = ctk.CTkLabel(frame, text="")
        self.auth_label.pack(pady=10)

    def show_register(self):
        """Display registration screen for creating new user accounts."""
        self.clear_window()

        frame = ctk.CTkFrame(self.root)
        frame.pack(expand=True, padx=40, pady=40)

        ctk.CTkLabel(frame, text="Register", font=("Arial", 24, "bold")).pack(pady=20)

        self.reg_user = ctk.CTkEntry(frame, placeholder_text="Username")
        self.reg_user.pack(pady=5)

        self.reg_pass = ctk.CTkEntry(frame, placeholder_text="Password", show="*")
        self.reg_pass.pack(pady=5)

        self.reg_pass2 = ctk.CTkEntry(frame, placeholder_text="Confirm Password", show="*")
        self.reg_pass2.pack(pady=5)

        ctk.CTkButton(frame, text="Register", command=self.register).pack(pady=10)
        ctk.CTkButton(frame, text="Back to Login", command=self.show_login).pack()

        self.reg_label = ctk.CTkLabel(frame, text="")
        self.reg_label.pack(pady=10)

    def login(self):
        """Handle login button click and authenticate user."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        success, msg = self.auth.login(username, password)
        self.auth_label.configure(text=msg)

        if success:
            self.root.after(1000, self.show_main_app)

    def register(self):
        """Handle registration button click and create new user account."""
        username = self.reg_user.get()
        password = self.reg_pass.get()
        confirm = self.reg_pass2.get()

        success, msg = self.auth.register(username, password, confirm)
        self.reg_label.configure(text=msg)

        if success:
            self.root.after(1000, self.show_login)

    def show_main_app(self):
        """Display main application screen with timer and task management."""
        self.clear_window()

        # Timer Section
        timer_frame = ctk.CTkFrame(self.root)
        timer_frame.pack(pady=10, padx=10, fill="x")

        self.timer_label = ctk.CTkLabel(timer_frame, text="25:00", font=("Arial", 36))
        self.timer_label.pack(pady=10)

        self.session_label = ctk.CTkLabel(timer_frame, text="Work Session")
        self.session_label.pack()

        btn_frame = ctk.CTkFrame(timer_frame)
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="Start", command=self.start_timer, width=80).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Pause", command=self.pause_timer, width=80).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Reset", command=self.reset_timer, width=80).pack(side="left", padx=5)

        # Tasks Section
        tasks_frame = ctk.CTkFrame(self.root)
        tasks_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Add Task
        add_frame = ctk.CTkFrame(tasks_frame)
        add_frame.pack(pady=5, padx=10, fill="x")

        self.task_entry = ctk.CTkEntry(add_frame, placeholder_text="Enter new task")
        self.task_entry.pack(side="left", fill="x", expand=True, padx=5)
        ctk.CTkButton(add_frame, text="Add", command=self.add_task, width=60).pack(side="right")

        # Tasks List
        self.tasks_list = ctk.CTkScrollableFrame(tasks_frame)
        self.tasks_list.pack(pady=10, padx=10, fill="both", expand=True)

        # Logout Button
        ctk.CTkButton(self.root, text="Logout", command=self.logout).pack(pady=10)

        # Setup timer callback
        self.timer.set_callback(self.update_timer)
        self.load_tasks()

    def start_timer(self):
        """Start the pomodoro timer."""
        self.timer.start()

    def pause_timer(self):
        """Pause the pomodoro timer."""
        self.timer.pause()

    def reset_timer(self):
        """Reset the pomodoro timer to initial state."""
        self.timer.reset()

    def update_timer(self, seconds, session_complete=False):
        """Update timer display when time changes or session completes."""
        formatted = self.timer.format_time(seconds)
        self.timer_label.configure(text=formatted)

        if session_complete:
            session_type = "Break" if self.timer.is_work_session else "Work"
            self.session_label.configure(text=f"{session_type} Session")

    def add_task(self):
        """Add a new task from the input field to the database."""
        task_text = self.task_entry.get()
        if task_text:
            self.db.add_task(self.auth.get_current_user_id(), task_text)
            self.task_entry.delete(0, "end")
            self.load_tasks()

    def load_tasks(self):
        """Load and display all tasks for the current user."""
        for widget in self.tasks_list.winfo_children():
            widget.destroy()

        tasks = self.db.get_user_tasks(self.auth.get_current_user_id())

        if not tasks:
            ctk.CTkLabel(self.tasks_list, text="No tasks yet").pack(pady=20)
            return

        for task_id, title, completed, pomodoro_count in tasks:
            task_frame = ctk.CTkFrame(self.tasks_list)
            task_frame.pack(fill="x", pady=2)

            text = f"✓ {title}" if completed else title
            text_color = "gray" if completed else "white"

            label = ctk.CTkLabel(task_frame, text=text, text_color=text_color)
            label.pack(side="left", padx=5)

            ctk.CTkLabel(task_frame, text=f"🍅 {pomodoro_count}").pack(side="left", padx=5)

            if not completed:
                ctk.CTkButton(task_frame, text="Complete", width=80,
                              command=lambda tid=task_id: self.complete_task(tid)).pack(side="right", padx=2)

            ctk.CTkButton(task_frame, text="Delete", width=60,
                          command=lambda tid=task_id: self.delete_task(tid)).pack(side="right", padx=2)

    def complete_task(self, task_id):
        """Mark a task as completed in the database."""
        self.db.complete_task(task_id)
        self.load_tasks()

    def delete_task(self, task_id):
        """Delete a task from the database."""
        self.db.delete_task(task_id)
        self.load_tasks()

    def logout(self):
        """Logout current user and return to login screen."""
        self.auth.logout()
        self.timer.pause()
        self.show_login()

    def clear_window(self):
        """Remove all widgets from the current window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        """Start the application main event loop."""
        self.root.mainloop()
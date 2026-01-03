"""
Application entry point
Creates and runs the main Pomodoro application.
"""

from gui import PomodoroApp

if __name__ == "__main__":
    app = PomodoroApp()
    app.run()
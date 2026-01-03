"""
Pomodoro timer implementation with work/break sessions.
Runs in a separate thread to avoid blocking the GUI.
"""

import threading
import time


class PomodoroTimer:
    """Manages the Pomodoro technique timer with work and break intervals."""

    def __init__(self):
        """Initialize timer with default work/break durations."""
        self.work_time = 25 * 60  # 25 minutes in seconds
        self.break_time = 5 * 60  # 5 minutes in seconds
        self.current_time = self.work_time
        self.is_running = False
        self.is_work_session = True
        self.callback = None

    def start(self):
        """Start the timer in a background thread."""
        if not self.is_running:
            self.is_running = True
            thread = threading.Thread(target=self.run_timer)
            thread.daemon = True
            thread.start()

    def pause(self):
        """Pause the running timer."""
        self.is_running = False

    def reset(self):
        """Reset timer to initial work session state."""
        self.is_running = False
        self.is_work_session = True
        self.current_time = self.work_time
        if self.callback:
            self.callback(self.current_time)

    def run_timer(self):
        """Main timer loop that counts down and handles session transitions."""
        while self.is_running and self.current_time > 0:
            time.sleep(1)
            self.current_time -= 1
            if self.callback:
                self.callback(self.current_time)

        if self.current_time == 0:
            self.session_complete()

    def session_complete(self):
        """Switch between work and break sessions when timer reaches zero."""
        self.is_work_session = not self.is_work_session
        self.current_time = self.break_time if not self.is_work_session else self.work_time
        if self.callback:
            self.callback(self.current_time, True)

    def format_time(self, seconds):
        """Convert seconds to MM:SS display format."""
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    def set_callback(self, callback):
        """Set callback function to update UI when timer changes."""
        self.callback = callback
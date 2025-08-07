import time
import threading
import argparse
from pynput import mouse, keyboard

class StayActiveService:
    """
    A service that periodically moves the mouse to prevent the system from becoming idle.
    It automatically pauses when it detects user activity (keyboard or mouse input)
    and resumes after a configurable delay of user inactivity.
    """
    def __init__(self, idle_delay_minutes=2):
        self.idle_delay_seconds = idle_delay_minutes * 60
        self.jiggle_interval_seconds = 30  # How often to jiggle when active
        self.last_activity_time = time.time()
        self.activity_lock = threading.Lock()
        self.mouse_controller = mouse.Controller()
        print(f"✅ Service initialized. Will jiggle mouse after {idle_delay_minutes} minute(s) of inactivity.")

    def _update_last_activity(self):
        """Thread-safe method to update the last activity timestamp."""
        with self.activity_lock:
            self.last_activity_time = time.time()

    def _on_activity(self, *args):
        """A single callback to handle any kind of user input."""
        self._update_last_activity()
        # print("User activity detected, pausing timer...") # Uncomment for debugging

    def _start_listeners(self):
        """Starts mouse and keyboard listeners in the background."""
        mouse_listener = mouse.Listener(on_move=self._on_activity, on_click=self._on_activity, on_scroll=self._on_activity)
        keyboard_listener = keyboard.Listener(on_press=self._on_activity)
        
        # Listeners run in their own threads
        mouse_listener.start()
        keyboard_listener.start()
        print("👂 Listening for your keyboard and mouse input...")

    def _jiggle_mouse(self):
        """Performs a small, non-disruptive mouse movement."""
        print(f"🏃 User idle for >{self.idle_delay_seconds / 60:.0f} mins. Jiggling mouse.")
        original_position = self.mouse_controller.position
        # Move a tiny amount and then move back
        self.mouse_controller.move(1, 1)
        time.sleep(0.1)
        self.mouse_controller.move(-1, -1)

    def run(self):
        """The main loop for the service."""
        self._start_listeners()
        try:
            while True:
                # Check if the idle threshold has been passed
                with self.activity_lock:
                    is_idle = (time.time() - self.last_activity_time) > self.idle_delay_seconds
                
                if is_idle:
                    self._jiggle_mouse()
                    # After jiggling, sleep for the jiggle interval before checking again
                    time.sleep(self.jiggle_interval_seconds)
                else:
                    # If user is active, check again in a second to conserve resources
                    time.sleep(1)

        except KeyboardInterrupt:
            print("\n🛑 Service stopped by user. Goodbye!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Keeps your computer active by jiggling the mouse. Pauses on user input."
    )
    parser.add_argument(
        "-d", "--delay",
        type=float,
        default=2.0,
        help="The user idle time in minutes before the mouse starts jiggling. Default is 2."
    )
    args = parser.parse_args()

    service = StayActiveService(idle_delay_minutes=args.delay)
    service.run()

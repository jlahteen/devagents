import sys
import time
import threading
import shutil
import textwrap
from monitoring.monitor import MonitorBase

class ConsoleMonitor2(MonitorBase):
    """Implements a console monitor with a status line at the bottom."""
    
    ESC = "\033"

    def __init__(self):
        self._stdout = sys.__stdout__
        self._start_time = time.time()
        self._running = True
        self._lock = threading.RLock()
        self._terminal_height = 0
        self._terminal_width = 0
        self._current_row = 1
        self._buffered_lines = []
        self._clear_screen()
        self._handle_resize()
        self._current_row = 1
        threading.Thread(target=self._resize_watcher, daemon=True).start()
        threading.Thread(target=self._update_status_line, daemon=True).start()

    def _set_scroll_region(self, top, bottom):
        self._stdout.write(f"{self.ESC}[{top};{bottom}r")

    def _reset_scroll_region(self):
        self._stdout.write(f"{self.ESC}[r")

    def _move_cursor(self, row, col):
        self._stdout.write(f"{self.ESC}[{row};{col}H")

    def _clear_line(self):
        self._stdout.write(f"{self.ESC}[2K")

    def _clear_screen(self):
        self._stdout.write(f"{self.ESC}[2J")
        self._stdout.flush()

    def _handle_resize(self):
        with self._lock:
            size = shutil.get_terminal_size()
            self._terminal_height = size.lines
            self._terminal_width = size.columns
            # Set scroll region to exclude the last row (status row)
            self._set_scroll_region(1, self._terminal_height - 1)
            self._move_cursor(self._terminal_height, 1)
            self._clear_line()
            self._stdout.flush()

    def _resize_watcher(self):
        while self._running:
            size = shutil.get_terminal_size()
            if size.lines != self._terminal_height or size.columns != self._terminal_width:
                self._handle_resize()
            time.sleep(0.5)

    def _update_status_line(self):
        # Hide cursor
        self._stdout.write(f"{self.ESC}[?25l")
        self._stdout.flush()

        try:
            while self._running:
                elapsed = int(time.time() - self._start_time)
                mins, secs = divmod(elapsed, 60)
                status = f"Elapsed: {mins:02d}:{secs:02d}"
                with self._lock:
                    self._move_cursor(self._terminal_height, 1)
                    self._clear_line()
                    # Fill line with white background
                    self._stdout.write(f"{self.ESC}[47m{' ' * self._terminal_width}{self.ESC}[0m")
                    self._move_cursor(self._terminal_height, 1)
                    self._stdout.write(f"{self.ESC}[30;47m{status}{self.ESC}[0m")
                    self._stdout.flush()
                time.sleep(1)
        finally:
            # Show cursor again
            self._stdout.write(f"{self.ESC}[?25h")
            self._stdout.flush()

    def write(self, data):
        with self._lock:
            wrapped_lines = textwrap.wrap(data, width=self._terminal_width, break_long_words=True)
            for line in wrapped_lines:
                self._buffered_lines.append(line)  # Buffer the line
                if self._current_row >= self._terminal_height:
                    self._stdout.write(f"{self.ESC}[1S")
                    self._current_row = self._terminal_height - 1
                self._move_cursor(self._current_row, 1)
                self._clear_line()
                self._stdout.write(line)
                self._current_row += 1
            self._stdout.flush()

    def close(self):
        self._running = False
        time.sleep(0.2)
        with self._lock:
            self._reset_scroll_region()
            self._clear_screen()
            self._stdout.write(f"{self.ESC}[?25h")
            # Print all buffered lines for scrolling, much faster
            if self._buffered_lines:
                self._stdout.write('\n'.join(self._buffered_lines) + '\n')
            self._stdout.flush()
            
    def flush(self):
        pass
    
    def set_current_agent(self, current_agent):
        """Sets the current agent in the monitor."""
        # This method can be implemented if needed for tracking agents
        pass


# Example usage
if __name__ == "__main__":
    ui = ConsoleMonitor2()

    try:
        for i in range(50):
            ui.write(f"This is the output line {i + 1}: " + "This is a long line of text that should wrap nicely across the terminal window.")
            time.sleep(0.3)
        for i in range(20000):
            ui.write(f"Output line {i + 1}")
            ui.write(f"{i} [INFO] Downloaded from central: https://repo.maven.apache.org/maven2/org/codehaus/plexus/plexus-utils/3.5.1/plexus-utils-3.5.1.pom (8.8 kB at 337 kB/s)")
    finally:
        time.sleep(2)
        ui.close()

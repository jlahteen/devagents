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

    def _write_and_buffer(self, line):
        if self._current_row - 1 < len(self._buffered_lines):
            self._buffered_lines[self._current_row - 1] = line
        else:
            self._buffered_lines.append(line)
        self._move_cursor(self._current_row, 1)
        self._clear_line()
        self._stdout.write(line)

    def _advance_row(self):
        self._current_row += 1
        if self._current_row >= self._terminal_height:
            self._stdout.write(f"{self.ESC}[1S")
            self._current_row = self._terminal_height - 1

    def write(self, data):
        with self._lock:
            if data == '\n':
                # Move to next line, scroll if necessary, and clear the new line
                self._advance_row()
                self._move_cursor(self._current_row, 1)
                self._clear_line()
                self._stdout.flush()
                return
            self._move_cursor(self._current_row, 1)
            if self._current_row - 1 < len(self._buffered_lines):
                current_line = self._buffered_lines[self._current_row - 1]
            else:
                current_line = ""
            lines = data.splitlines() or [""]
            first_line = lines[0]
            appended = current_line + first_line
            wrapped = textwrap.wrap(appended, width=self._terminal_width, break_long_words=True)
            # Write and buffer the first wrapped line
            self._write_and_buffer(wrapped[0])
            # Handle any wrapped overflow from the first line
            for wline in wrapped[1:]:
                self._advance_row()
                self._write_and_buffer(wline)
            # Now handle the rest of the lines, except the last
            for line in lines[1:-1]:
                self._advance_row()
                wrapped_rest = textwrap.wrap(line, width=self._terminal_width, break_long_words=True)
                for wline in wrapped_rest:
                    self._write_and_buffer(wline)
                    self._advance_row()
            # For the last line, just append to the buffer but do not move the row after
            if len(lines) > 1:
                last_line = lines[-1]
                wrapped_last = textwrap.wrap(last_line, width=self._terminal_width, break_long_words=True)
                for idx, wline in enumerate(wrapped_last):
                    if idx == 0:
                        self._advance_row()
                    self._write_and_buffer(wline)
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

    def get_terminal_height_width(self):
        """Returns the current terminal height and width as a tuple."""

        with self._lock:
            return (self._terminal_height, self._terminal_width)


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

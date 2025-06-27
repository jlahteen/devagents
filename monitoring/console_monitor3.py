import sys
import textwrap
import threading
import time
import shutil
from monitoring.monitor import MonitorBase

class ConsoleMonitor3(MonitorBase):
    """A monitor that uses the console for showing the agent conversation with a fixed status line at the bottom, using ANSI codes (no curses)."""

    ESC = "\033"

    def __init__(self):
        """Initializes the ConsoleMonitor instance."""
        self._running = True
        self._started = time.time()
        self._spinner_chars = ["|", "/", "-", "\\"]
        self._spinner_idx = 0
        self._current_agent = "<no agent>"
        self._stdout = sys.__stdout__
        self._screen_lock = threading.RLock()
        self._spinner_char_last_updated = 0
        self.original_lines = [""]
        self.wrapped_lines = [""]
        self._terminal_height = 0
        self._terminal_width = 0
        self._current_row = 1
        self._clear_screen()
        self._handle_resize()
        self._current_row = 1
        # Start the resize listener thread
        self._resize_thread = threading.Thread(target=self._resize_thread_main, daemon=True)
        self._resize_thread.start()
        # Start the status updater thread
        self._status_updater_thread = threading.Thread(target=self._status_updater_thread_main, daemon=True)
        self._status_updater_thread.start()
        self._hide_cursor()
        self._stdout.flush()
        
    def _hide_cursor(self):
        self._stdout.write(f"{self.ESC}[?25l")
        
    def _show_cursor(self):
        self._stdout.write(f"{self.ESC}[?25h")

    def _set_scroll_region(self, top, bottom):
        self._stdout.write(f"{self.ESC}[{top};{bottom}r")

    def _reset_scroll_region(self):
        self._stdout.write(f"{self.ESC}[r")

    def _move_cursor(self, row, col):
        self._stdout.write(f"{self.ESC}[{row};{col}H")

    def _scroll_up(self):
        self._stdout.write(f"{self.ESC}[1S")

    def _clear_line(self):
        self._stdout.write(f"{self.ESC}[2K")

    def _clear_screen(self):
        self._stdout.write(f"{self.ESC}[2J")
        self._stdout.flush()

    def _handle_resize(self):
        size = shutil.get_terminal_size()
        self._terminal_height = size.lines
        self._terminal_width = size.columns
        # Set scroll region to exclude the last row (status row)
        self._set_scroll_region(1, self._terminal_height - 1)
        self._move_cursor(self._terminal_height, 1)
        self._clear_line()
        self._stdout.flush()

    def _resize_thread_main(self):
        while self._running:
            size = shutil.get_terminal_size()
            if size.lines != self._terminal_height or size.columns != self._terminal_width:
                with self._screen_lock:
                    self._handle_resize()
                    self.wrapped_lines = self._wrap_lines(self.original_lines, self._terminal_width)
                    self._render_terminal()
            time.sleep(0.5)

    def _render_terminal(self):
        self._clear_screen()
        self._move_cursor(1, 1)
        first_line_to_render = max(0, len(self.wrapped_lines) - (self._terminal_height - 1))
        self._current_row = 1
        for i in range(first_line_to_render, len(self.wrapped_lines)):
            self._render_line(self.wrapped_lines[i])
            if i < len(self.wrapped_lines) - 1:
                self._render_new_line()
        self._stdout.flush()

    def set_current_agent(self, current_agent):
        self._current_agent = current_agent

    def write(self, text):
        """Writes a specified text to the console."""
        with self._screen_lock:
            if text == "":
                return
            elif text == "\n":
                self._write_new_line()
                return
            elif "\n" not in text:
                self._write_chars(text)
                return
            else:
                new_lines = text.split("\n")
                for i in range(len(new_lines)):
                    self._write_chars(new_lines[i])
                    if i < len(new_lines) - 1:
                        self._write_new_line()

    def flush(self):
        pass

    def close(self):
        self._running = False
        self._status_updater_thread.join()
        self._resize_thread.join()
        with self._screen_lock:
            self._reset_scroll_region()
            self._clear_screen()
            self._show_cursor()
            # Print the wrapped lines to the console
            if self.wrapped_lines:
                self._stdout.write('\n'.join(self.wrapped_lines) + '\n')
            self._stdout.flush()

    def get_terminal_height_width(self):
        """Returns the current terminal height and width as a tuple."""

        with self._screen_lock:
            return (self._terminal_height, self._terminal_width)

    def _write_new_line(self):
        self.original_lines.append("")
        self.wrapped_lines.append("")
        self._render_new_line()
        self._move_cursor(self._current_row, 1)
        self._clear_line()
        self._stdout.flush()

    def _write_chars(self, chars):
        wrap_width = self._terminal_width
        self.original_lines[-1] += chars
        if len(self.wrapped_lines[-1]) + len(chars) <= wrap_width:
            self.wrapped_lines[-1] += chars
            self._render_line(self.wrapped_lines[-1])
        else:
            wrapped_lines = self._wrap_lines([self.wrapped_lines[-1] + chars], wrap_width)
            self.wrapped_lines.pop()
            for i, wline in enumerate(wrapped_lines):
                self.wrapped_lines.append(wline)
                self._render_line(wline)
                if i < len(wrapped_lines) - 1:
                    self._render_new_line()
        self._stdout.flush()

    def _wrap_lines(self, lines, max_width):
        wrapped_lines = []
        for line in lines:
            if len(line) <= max_width:
                wrapped_lines.append(line)
            else:
                wrapped_lines.extend(textwrap.wrap(line, max_width, break_long_words=True))
        return wrapped_lines

    def _render_line(self, line):
        self._move_cursor(self._current_row, 1)
        self._clear_line()
        self._stdout.write(line)

    def _render_new_line(self):
        self._current_row += 1
        if self._current_row >= self._terminal_height:
            self._scroll_up()
            self._current_row = self._terminal_height - 1

    def _get_status_line(self):
        if time.time() - self._spinner_char_last_updated > 0.25:
            self._spinner_idx += 1
            self._spinner_char_last_updated = time.time()
        status_line = "DevAgents | "
        elapsed = time.time() - self._started
        status_line += time.strftime("%H:%M:%S", time.gmtime(elapsed)) + " | "
        status_line += f"{self._current_agent} working"
        status_line += " " + self._spinner_chars[self._spinner_idx % len(self._spinner_chars)]
        return status_line

    def _update_status_line(self):
        status_line = self._get_status_line()
        with self._screen_lock:
            self._move_cursor(self._terminal_height, 1)
            self._clear_line()
            # Fill line with white background
            self._stdout.write(f"{self.ESC}[47m{' ' * self._terminal_width}{self.ESC}[0m")
            self._move_cursor(self._terminal_height, 1)
            self._stdout.write(f"{self.ESC}[30;47m{status_line[:self._terminal_width]}{self.ESC}[0m")
            self._stdout.flush()

    def _status_updater_thread_main(self):
        while self._running:
            self._update_status_line()
            time.sleep(0.25)


import curses
import sys
import textwrap
import threading
import time


class ConsoleMonitor:
    """A monitor that uses the console for showing the agent conversation with a fixed status line at the bottom."""

    def __init__(self):
        """Initializes the ConsoleMonitor instance."""

        self._console_monitor_running = True
        self._started = time.time()
        self._spinner_chars = ["|", "/", "-", "\\"]
        self._spinner_idx = 0
        self._current_agent = "<no agent>"
        # Set up curses
        self.stdscr = curses.initscr()
        self.stdscr.clear()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        self.stdscr.scrollok(True)
        self.stdscr.move(0, 0)
        self.stdscr.refresh()

        # Hide the cursor
        curses.curs_set(0)

        # Set up the color for the status line
        if curses.has_colors():
            curses.start_color()
            curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

        # Store original unwrapped lines and wrapped lines separately
        self.original_lines = [""]
        self.wrapped_lines = [""]

        # Threading lock for screen updates
        self._screen_lock = threading.RLock()

        # Start the resize listener thread
        self._resize_thread = threading.Thread(target=self._resize_thread_main, daemon=True)
        self._resize_thread.start()

        # Start the status line updater thread
        self._spinner_char_last_updated = 0
        self._status_updater_thread = threading.Thread(target=self._status_line_thread_main, daemon=True)
        self._status_updater_thread.start()

    def set_current_agent(self, current_agent):
        """Sets the currently working agent."""

        self._current_agent = current_agent

    def write(self, text):
        """Writes a specified text to the console."""

        if text == "":
            # Text is empty, do nothing
            return
        elif text == "\n":
            # Write a new line
            self._write_new_line()
            return
        elif "\n" not in text:
            # Write just chars without new lines
            self._write_chars(text)
            return
        else:
            # Write a multi-line text
            new_lines = text.split("\n")
            for i in range(len(new_lines)):
                self._write_chars(new_lines[i])
                if i < len(new_lines) - 1:
                    # This is not the last line, write a new line
                    self._write_new_line()

    def flush(self):
        """Flushes the console output. This is a no-op for this console."""

        pass

    def close(self):
        """Closes the console and restores the terminal settings."""

        # Stop the threads
        self._console_monitor_running = False
        self._status_updater_thread.join()
        self._resize_thread.join()
        # Clear the status line
        height = self.stdscr.getmaxyx()[0]
        self.stdscr.move(height - 1, 0)
        self.stdscr.clrtoeol()
        self.stdscr.refresh()
        # Restore terminal settings
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.curs_set(1)
        curses.endwin()
        # Print the wrapped lines to the console
        sys.__stdout__.write("\n")
        for line in self.wrapped_lines:
            sys.__stdout__.write(line + "\n")

    def _write_new_line(self):
        """Writes a new line to the console."""

        self.original_lines.append("")
        self.wrapped_lines.append("")
        self._render_new_line()

    def _write_chars(self, chars):
        """
        Writes chars to the console, wrapping them to the next line, if necessary.
        The chars are not assumed to contain any new line characters.
        """

        # Set the wrap width
        wrap_width = self.stdscr.getmaxyx()[1] - 1
        # Update the original lines
        self.original_lines[-1] += chars
        # Update the wrapped lines and render the chars
        if len(self.wrapped_lines[-1]) + len(chars) <= wrap_width:
            # The chars fit in the current line
            self.wrapped_lines[-1] += chars
            self._render_chars(chars)
        else:
            # The chars will wrap to several lines
            wrapped_lines = self._wrap_lines([self.wrapped_lines[-1] + chars], wrap_width)
            # Remove the last line from the wrapped lines, it will be added later
            self.wrapped_lines.pop()
            # Move the cursor to the beginning of the current line
            self.stdscr.move(self.stdscr.getyx()[0], 0)
            # Update and render the wrapped lines
            for i in range(len(wrapped_lines)):
                self.wrapped_lines.append(wrapped_lines[i])
                self._render_chars(wrapped_lines[i])
                if i < len(wrapped_lines) - 1:
                    self._render_new_line()

    def _wrap_lines(self, lines, max_width):
        """
        Wraps the specified input lines to the specified max_width.
        Returns a list of the wrapped lines.
        """

        wrapped_lines = []
        for line in lines:
            if len(line) <= max_width:
                wrapped_lines.append(line)
            else:
                wrapped_lines.extend(textwrap.wrap(line, max_width, break_long_words=False))
        return wrapped_lines

    def _render_new_line(self):
        """Renders a new line to the console."""

        height = self.stdscr.getmaxyx()[0]
        cur_y = self.stdscr.getyx()[0]
        if cur_y >= height - 2:
            # The cursor is at the last line or even below
            # Scroll up
            self.stdscr.scroll(1)
            # Set the cursor at the beginning of the last line
            self.stdscr.move(height - 2, 0)
            self.stdscr.clrtoeol()
        else:
            # There are still lines below
            self.stdscr.move(cur_y + 1, 0)
        # Update the scrolled status line
        self._update_status_line()
        self.stdscr.refresh()

    def _render_chars(self, chars):
        """Renders chars to the console, chars are not assumed to contain new lines."""

        self.stdscr.addstr(chars)
        self.stdscr.refresh()

    def _resize_thread_main(self):
        """A main function for the resize thread. Listens for resize events and resizes the console window if necessary."""

        self.stdscr.nodelay(True)
        while self._console_monitor_running:
            key = self.stdscr.getch()
            if key == curses.KEY_RESIZE:
                with self._screen_lock:
                    # Get the new size of the console
                    new_height, new_width = self.stdscr.getmaxyx()
                    # Rewrap the original lines to the new width
                    self.wrapped_lines = self._wrap_lines(self.original_lines, new_width - 1)
                    # Clear the screen and render the last new_height - 1 lines
                    self.stdscr.clear()
                    self.stdscr.move(0, 0)
                    first_line_to_render = max(0, len(self.wrapped_lines) - (new_height - 1))
                    for i in range(first_line_to_render, len(self.wrapped_lines)):
                        self._render_chars(self.wrapped_lines[i])
                        if i < len(self.wrapped_lines) - 1:
                            self._render_new_line()
            time.sleep(0.05)

    def _get_status_line(self):
        """Gets the current status line text."""

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
        """Updates the status line at the bottom of the console. This method does not refresh the screen."""

        status_line = self._get_status_line()
        height, width = self.stdscr.getmaxyx()
        # Save the current cursor position
        orig_y, orig_x = self.stdscr.getyx()
        self.stdscr.move(height - 1, 0)
        # Fill the line with spaces to clear it
        self.stdscr.addstr(" " * (width - 1), curses.color_pair(1))
        self.stdscr.move(height - 1, 0)
        # Write the status text, truncated to width - 1
        self.stdscr.addstr(status_line[: width - 1], curses.color_pair(1))
        # Restore original cursor position
        self.stdscr.move(orig_y, orig_x)

    def _status_line_thread_main(self):
        """A main function for the status line updater thread. The thread keeps updating the status line with a spinner."""

        while self._console_monitor_running:
            with self._screen_lock:
                self._update_status_line()
                self.stdscr.refresh()
            time.sleep(0.25)

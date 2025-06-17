import curses
import sys
import textwrap
import threading
import time


class ConsoleMonitor:
    """A monitor that uses console for showing the agent conversation with a fixed status line at the bottom."""

    def __init__(self):
        """Initializes the ConsoleMonitor instance."""

        self._console_monitor_running = True
        self._started = time.time()

        self._spinner_chars = ["|", "/", "-", "\\"]
        self._spinner_idx = 0

        self._current_agent = "<no agent>"

        # Set up curses properly
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
        # Set up color for status line
        if curses.has_colors():
            curses.start_color()
            curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

        # Store original unwrapped text and wrapped lines separately
        self.original_lines = []
        self.wrapped_lines = []

        # Threading lock for screen updates
        self._screen_lock = threading.RLock()

        # Start the resize listener thread
        self._resize_thread = threading.Thread(target=self._resize_thread_main, daemon=True)
        self._resize_thread.start()

        # Start the status line updater thread
        self._spinner_char_last_updated = 0
        self._status_updater_thread = threading.Thread(target=self._status_line_thread_main, daemon=True)
        self._status_updater_thread.start()

    def set_current_agent(self, agent_name):
        """Sets the current agent name."""

        self._current_agent = agent_name
        
    def wrap_lines(self, lines, max_width):
        """
        Wraps each line in the input lines to the specified max_width.
        Returns a new list of wrapped lines.
        """

        wrapped = []
        for line in lines:
            if len(line) <= max_width:
                wrapped.append(line)
            else:
                wrapped.extend(textwrap.wrap(line, max_width))
        return wrapped

    def _render_content(self, new_wrapped_lines):
        """Renders new wrapped lines to the console, scrolls if needed."""

        with self._screen_lock:
            height, _ = self.stdscr.getmaxyx()
            usable_height = height - 1
            for line in new_wrapped_lines:
                cur_y, _ = self.stdscr.getyx()
                if cur_y == usable_height - 1:
                    # The console is full, scroll up
                    self.stdscr.scroll(1)
                    # self.stdscr.move(cur_y - 1, 0)
                    self.stdscr.clrtoeol()
                    self.stdscr.addstr(line)
                    self.stdscr.move(cur_y, 0)
                else:
                    # There is still space below, move down
                    # self.stdscr.move(cur_y + 1, 0)
                    self.stdscr.clrtoeol()
                    self.stdscr.addstr(line)
                    self.stdscr.move(cur_y + 1, 0)
            self._update_status_line()
            self.stdscr.refresh()

    def _render_new_line(self):
        """Renders a new line feed in the console, scrolling if needed."""

        with self._screen_lock:
            height, _ = self.stdscr.getmaxyx()
            cur_y, _ = self.stdscr.getyx()
            if cur_y >= height - 2:
                # The cursor is at the last line or even below
                # Scroll up
                self.stdscr.scroll(1)
                # Set the cursor at the beginning of the last line
                self.stdscr.move(height - 2, 0)
                self.stdscr.clrtoeol()
            else:
                self.stdscr.move(cur_y + 1, 0)
            self._update_status_line()
            self.stdscr.refresh()

    def _render_chars(self, chars):
        """Renders chars to the console, chars are not assumed to contain newlines."""

        with self._screen_lock:
            self.stdscr.addstr(chars)
            self._update_status_line()
            self.stdscr.refresh()

    def write(self, text):
        """Prints a specified text to the console."""

        _, width = self.stdscr.getmaxyx()
        wrap_width = max(10, width - 1)
        if text == "":
            # If the text is empty, do nothing
            return
        elif text == '\n':
            # Render a new line
            self._render_new_line()
            self.original_lines.append("")
            self.wrapped_lines.append("")
            return
        elif len(text) == 1:
            # If the text is a single character, add it to the last line
            if len(self.original_lines) == 0:
                self.original_lines.append(text)
                self.wrapped_lines.append(text)
            else:
                self.original_lines[-1] += text
                if len(self.wrapped_lines[-1]) >= wrap_width:
                    self.wrapped_lines.append(text)
                    self._render_new_line()
                else:
                    self.wrapped_lines[-1] += text
            self._render_chars(text)
            return
        else:
            # Split text into lines by a new line character
            new_lines = text.split("\n")
            # Add the new lines to the original lines
            # The first line should be appended to the last line if it exists
            if self.original_lines:
                self.original_lines[-1] += new_lines[0]
            else:
                self.original_lines.append(new_lines[0])
            # For the rest of the lines, add as new entries
            if len(new_lines) > 1:
                self.original_lines.extend(new_lines[1:])
            # Wrap the lines by the current terminal width
            new_wrapped_lines = self.wrap_lines(new_lines, wrap_width)
            # Render the first wrapped line            
            if not self.wrapped_lines:
                start = 0
            else:            
                if len(self.wrapped_lines[-1]) + len(new_wrapped_lines[0]) <= wrap_width:
                    # The first wrapped line fits in the last line
                    self._render_chars(new_wrapped_lines[0])
                    self.wrapped_lines[-1] += new_wrapped_lines[0]
                    if len(new_wrapped_lines) > 1:
                        self._render_new_line()
                else:
                    # Weed need an additional line to render the first wrapped line
                    space_left = wrap_width - len(self.wrapped_lines[-1])
                    self.wrapped_lines[-1] += new_wrapped_lines[0][:space_left]
                    self._render_chars(new_wrapped_lines[0][:space_left])
                    remainder = new_wrapped_lines[0][space_left:]
                    if remainder:
                        self.wrapped_lines.append(remainder)
                        self._render_new_line()
                        self._render_chars(remainder)
                start = 1
            # Render the rest of the wrapped lines
            for i in range(start, len(new_wrapped_lines)):
                self.wrapped_lines.append(new_wrapped_lines[i])
                self._render_chars(new_wrapped_lines[i])
                if i < len(new_wrapped_lines) - 1:
                    self._render_new_line()

    def flush(self):
        """Flushes the console output. This is a no-op for this console."""

        pass

    def _resize_thread_main(self):
        """Listens for resize events and resizes the console window when such events are received."""

        self.stdscr.nodelay(True)
        while self._console_monitor_running:
            try:
                key = self.stdscr.getch()
                if key == curses.KEY_RESIZE:
                    self.handle_resize()
                    self._render_content()
                time.sleep(0.05)
            except Exception:
                pass

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
        # Save current cursor position
        orig_y, orig_x = self.stdscr.getyx()
        self.stdscr.move(height - 1, 0)
        # Fill the line with spaces in the color
        self.stdscr.addstr(' ' * (width - 1), curses.color_pair(1))
        self.stdscr.move(height - 1, 0)
        # Write the status text, truncated to width-1
        self.stdscr.addstr(status_line[:width - 1], curses.color_pair(1))
        # Restore original cursor position
        self.stdscr.move(orig_y, orig_x)

    def _status_line_thread_main(self):
        """Thread to update the status line with a spinner."""

        while self._console_monitor_running:
            with self._screen_lock:
                self._update_status_line()
                self.stdscr.refresh()
            time.sleep(0.25)

    def close(self):
        """Closes the console and restores terminal settings."""

        # Stop the threads
        self._console_monitor_running = False
        self._status_updater_thread.join()
        self._resize_thread.join()
        # Clear the status line
        height, _ = self.stdscr.getmaxyx()
        self.stdscr.move(height - 1, 0)
        self.stdscr.clrtoeol()
        self.stdscr.refresh()
        # Restore terminal settings
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.curs_set(1)
        curses.endwin()
        # Print the original lines to the console
        sys.__stdout__.write("\n")
        for line in self.wrapped_lines:
            sys.__stdout__.write(line + "\n")

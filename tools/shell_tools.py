import shutil
import subprocess
import sys
import threading
import time
from io import StringIO

from utils.misc import print_tool_error, print_tool_use
from utils.tee import Tee

file_lock = threading.Lock()

_DEFAULT_TERMINAL_WIDTH = 120
_DEFAULT_TERMINAL_HEIGHT = 24
_MIN_CONTENT_WIDTH = 20
_DEFAULT_OUTPUT_INDENT = 5
_DEFAULT_INACTIVITY_TIMEOUT = 150


def detect_terminal_width(default=_DEFAULT_TERMINAL_WIDTH):
    try:
        return shutil.get_terminal_size(fallback=(default, _DEFAULT_TERMINAL_HEIGHT)).columns
    except Exception:
        return default


class StreamingFormatter:
    def __init__(self, writer, indent, max_width=None):
        self._writer = writer
        self._indent = " " * indent
        term_width = max_width or detect_terminal_width()
        # Reserve one char to prevent automatic terminal line wraps with the maximum terminal width
        self._max_width = max(term_width - 1, indent + _MIN_CONTENT_WIDTH)
        self._content_width = self._max_width - indent
        self._buffer = ""

    def _flush(self, newline=True):
        if self._buffer:
            self._writer.write(self._indent + self._buffer)
            if newline:
                self._writer.write("\n")
            self._buffer = ""

    def write_char(self, char: str):
        # Preserve explicit newlines from the process
        if char == "\n":
            self._flush(newline=True)
            return
        self._buffer += char
        # Soft wrap at word boundaries, hard wrap if word is too long
        while len(self._buffer) >= self._content_width:
            # Try to find the last space within the content width for a soft wrap
            chunk = self._buffer[: self._content_width]
            last_space = chunk.rfind(" ")
            if last_space > 0:
                # Soft wrap: break at word boundary
                self._writer.write(self._indent + chunk[:last_space] + "\n")
                self._buffer = self._buffer[last_space + 1 :]
            else:
                # Hard wrap: no space found, break at character boundary
                self._writer.write(self._indent + chunk + "\n")
                self._buffer = self._buffer[self._content_width :]

    def flush(self):
        self._flush(newline=True)


def run_command(command: str) -> str:
    """Runs a specified command, streams all output to the console, and returns the full output."""

    with file_lock:
        print_tool_use(command)

        output = StringIO()
        tee = Tee(sys.stdout, output)

        formatter = StreamingFormatter(
            writer=tee,
            indent=_DEFAULT_OUTPUT_INDENT,
        )

        try:
            process = subprocess.Popen(
                command,
                shell=True,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=0,
                encoding="utf-8",
                errors="replace",
            )

            last_activity = time.time()
            timed_out = False

            def watchdog():
                """Monitors for inactivity and kills the process if it is stuck."""

                nonlocal timed_out
                while process.poll() is None:
                    time.sleep(1)
                    if time.time() - last_activity > _DEFAULT_INACTIVITY_TIMEOUT:
                        timed_out = True
                        process.kill()
                        break

            watchdog_thread = threading.Thread(target=watchdog, daemon=True)
            watchdog_thread.start()

            while True:
                char = process.stdout.read(1)
                if not char:
                    break
                last_activity = time.time()
                formatter.write_char(char)
                tee.flush()

            formatter.flush()

            return_code = process.wait()
            process.stdout.close()

            output_text = output.getvalue()

            if timed_out:
                error_msg = f"run_command ERROR: Command '{command}' had no output for {_DEFAULT_INACTIVITY_TIMEOUT} seconds (likely waiting for user input)"
                print_tool_error(error_msg)
                return error_msg + "\n" + output_text
            elif return_code == 0:
                print()
                return output_text
            else:
                error_msg = f"run_command ERROR: Command '{command}' reported an error (code {return_code})"
                print_tool_error(error_msg)
                return error_msg + "\n" + output_text

        except Exception as e:
            error_msg = f"run_command ERROR: Failed to run the command '{command}': {str(e)}"
            print_tool_error(error_msg)
            return error_msg

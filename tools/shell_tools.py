import shutil
import subprocess
import sys
import threading
from io import StringIO

from utils.misc import print_tool_error, print_tool_use
from utils.tee import Tee

file_lock = threading.Lock()

DEFAULT_TERMINAL_WIDTH = 120
DEFAULT_TERMINAL_HEIGHT = 24
MIN_CONTENT_WIDTH = 20
DEFAULT_OUTPUT_INDENT = 5


def detect_terminal_width(default=DEFAULT_TERMINAL_WIDTH):
    try:
        return shutil.get_terminal_size(fallback=(default, DEFAULT_TERMINAL_HEIGHT)).columns
    except Exception:
        return default


class StreamingFormatter:
    def __init__(self, writer, indent, max_width=None):
        self._writer = writer
        self._indent = " " * indent
        term_width = max_width or detect_terminal_width()
        # Reserve one char to prevent automatic terminal line wraps with the maximum terminal width
        self._max_width = max(term_width - 1, indent + MIN_CONTENT_WIDTH)
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
            indent=DEFAULT_OUTPUT_INDENT,
        )

        try:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=0,
                encoding="utf-8",
                errors="replace",
            )

            while True:
                char = process.stdout.read(1)
                if not char:
                    break
                formatter.write_char(char)
                tee.flush()

            formatter.flush()

            return_code = process.wait()
            process.stdout.close()

            output_text = output.getvalue()

            if return_code == 0:
                print()
                return output_text
            else:
                error_msg = f"run_command ERROR: Command '{command}' reported an error " f"(code {return_code})"
                print_tool_error(error_msg)
                return error_msg + "\n" + output_text

        except Exception as e:
            error_msg = f"run_command ERROR: Failed to run the command '{command}': {str(e)}"
            print_tool_error(error_msg)
            return error_msg

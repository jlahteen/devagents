import datetime
import os
from pathlib import Path


def print_yellow(text: str) -> None:
    """Prints a given text in yellow color to the console."""

    print(f"\033[93m{text}\033[0m")


def print_red(text: str) -> None:
    """Prints a given text in red color to the console."""

    print(f"\033[91m{text}\033[0m")


def print_green(text: str) -> None:
    """Prints a given text in green color to the console."""

    print(f"\033[0;32m{text}\033[0m")


def print_tool_error(message: str) -> None:
    """Prints a tool error message with icon in light yellow color."""

    try:
        print(f"\033[93m🔧 {message}\033[0m")
    except UnicodeEncodeError:
        print(f"\033[93m[TOOL] {message}\033[0m")


def print_tool_use(message: str) -> None:
    """Prints a tool usage message in gray color."""

    try:
        print(f"\033[90m🔧 {message}\033[0m")
    except UnicodeEncodeError:
        print(f"\033[90m[TOOL] {message}\033[0m")


def generate_timestamp():
    """Generates a timestamp in the format of YYYYMMDDHHMMSSmmm."""

    now = datetime.datetime.now()
    return now.strftime("%Y%m%d%H%M%S") + f"{int(now.microsecond/1000):03d}"


def to_os_path(windows_path: str) -> str:
    """
    Converts a Windows-style path to a Unix-style path if running on a Unix system.
    Also removes the .exe extension if present.
    """

    if os.name != "nt":
        # Replace backslashes with forward slashes
        unix_path = windows_path.replace("\\", "/")
        # Remove the drive letter from the path
        if unix_path[1] == ":":
            unix_path = unix_path[2:]
        # Remove the .exe extension if present
        if unix_path.endswith(".exe"):
            unix_path = unix_path[:-4]
        return unix_path
    else:
        return windows_path


def is_valid_file_path(file_path: str) -> bool:
    """
    Checks if a string is a valid file path that should be attempted to read.

    Returns True if the string:
    - Has a parent directory (e.g., folder/file.txt)
    - Contains no spaces (single word, e.g., file.txt or README)

    Returns False for multi-word text (likely a prompt).
    """

    try:
        path = Path(file_path)

        # Treat as file path if it has a parent directory
        if path.parent != Path("."):
            return True

        # Treat as file path if it's a single word (no spaces)
        if " " not in file_path.strip():
            return True

        return False
    except (ValueError, OSError):
        # Invalid path format
        return False

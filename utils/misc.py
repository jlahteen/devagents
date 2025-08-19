import datetime
import os


def print_yellow(text: str) -> None:
    """Prints a given text in yellow color to the console."""

    print(f"\033[93m{text}\033[0m")


def print_red(text: str) -> None:
    """Prints a given text in red color to the console."""

    print(f"\033[91m{text}\033[0m")


def print_green(text: str) -> None:
    """Prints a given text in green color to the console."""

    print(f"\033[0;32m{text}\033[0m")


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

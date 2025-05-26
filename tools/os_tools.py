import platform
import sys


def to_os_path(windows_path: str) -> str:
    """
    Converts a Windows-style path to a Unix-style path if running on a Unix system.
    Also removes the .exe extension if present.
    """

    if platform.system() != "Windows":
        # Replace backslashes with forward slashes
        unix_path = windows_path.replace("\\", "/")
        # Remove the .exe extension if present
        if unix_path.endswith(".exe"):
            unix_path = unix_path[:-4]
        return unix_path
    else:
        return windows_path


def get_os_type() -> str:
    """
    Returns the current operating system type.
    """

    os_name = platform.system()
    if os_name == "Darwin":
        return "macOS"
    else:
        return os_name

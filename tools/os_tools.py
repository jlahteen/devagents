import sys


def to_os_path(windows_path: str) -> str:
    """
    Converts a Windows-style path to a Unix-style path if running on a Unix system.
    Also removes the .exe extension if present.
    """

    if get_os_type() != "Windows":
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


def get_os_type() -> str:
    """
    Returns the current operating system type.
    """

    os_name = sys.platform.lower()
    if os_name.startswith("nt") or os_name.startswith("win"):
        return "Windows"
    elif os_name.startswith("darwin") or os_name.startswith("mac"):
        return "macOS"
    else:
        return "Linux"

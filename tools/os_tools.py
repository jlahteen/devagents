import sys
from datetime import datetime


def get_timestamp() -> str:
    """Returns the current date and time in the YYYY-MM-DD HH:MM format."""

    return datetime.now().strftime("%Y-%m-%d %H:%M")


def get_os_type() -> str:
    """Returns the current operating system type."""

    os_name = sys.platform.lower()
    if os_name.startswith("nt") or os_name.startswith("win"):
        return "Windows"
    elif os_name.startswith("darwin") or os_name.startswith("mac"):
        return "macOS"
    else:
        return "Linux"

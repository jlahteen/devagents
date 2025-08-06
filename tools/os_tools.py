import sys


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

import datetime


def print_yellow(text: str) -> None:
    """Prints a given text in yellow color to the console."""

    print(f"\033[93m{text}\033[0m")


def print_red(text: str) -> None:
    """Prints a given text in red color to the console."""

    print(f"\033[91m{text}\033[0m")


def print_green(text: str) -> None:
    """Prints a given text in green color to the console."""

    print(f"\033[0;32m{text}\033[0m")


def over_to(agent_name: str) -> str:
    """Prints a message indicating the next agent to speak."""

    print_yellow(f"Over to {agent_name}...")
    return agent_name


def generate_timestamp():
    """Generates a timestamp in the format of YYYYMMDDHHMMSSmmm."""

    now = datetime.datetime.now()
    return now.strftime("%Y%m%d%H%M%S") + f"{int(now.microsecond/1000):03d}"

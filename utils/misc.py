import sys


def print_yellow(text: str) -> None:
    """Prints a given text in yellow color to the console."""

    print(f"\033[93m{text}\033[0m")


def over_to(agent_name: str) -> str:
    """Prints a message indicating the next agent to speak."""

    print_yellow(f"Over to {agent_name}...")
    return agent_name

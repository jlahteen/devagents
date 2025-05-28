import pyfiglet

BUILD = "Build __BUILD__"


def say_hello():
    """Prints a welcome message with ASCII art for "DevAgents"."""

    # Generate ASCII art for "DevAgents"
    ascii_art = pyfiglet.figlet_format("DevAgents")

    # Get the width of the ASCII art to create a consistent border around it
    width = len(max(ascii_art.splitlines(), key=len))
    border_line = "=" * (width + 4)

    # Print the box and message with some fancy formatting
    print()
    print(border_line)
    for line in ascii_art.splitlines():
        print(f"/ {line.ljust(width)} \\")
    print(f"/ {''.ljust(width)} \\")
    print(f"/ {BUILD.center(width)} \\")
    print(border_line)
    print(" ✨  Hey! We are a software team of AI agents.  ✨")
    print(" ✨       Let's create something together!      ✨")
    print()


if __name__ == "__main__":
    say_hello()

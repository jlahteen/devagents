import pyfiglet

BUILD = "Build __BUILD__"
HOME_PAGE = "https://github.com/jlahteen/devagents"


def print_home_page(width):
    """Prints the HOME_PAGE centered within the given width."""

    home_page_link = f"\033[38;2;59;110;234m{HOME_PAGE}\033[0m"
    left_padding = (width - len(HOME_PAGE)) // 2
    right_padding = width - len(HOME_PAGE) - left_padding
    print(f"/ {' ' * left_padding}{home_page_link}{' ' * right_padding} \\")


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
    print_home_page(width)
    print(f"/ {''.ljust(width)} \\")
    print(border_line)
    print(" ✨  Hey! We're AI agents that build software.  ✨")
    print(" ✨       Let's create something together!      ✨")
    print(" ✨   Always verify and test AI written code.   ✨")
    print()


if __name__ == "__main__":
    say_hello()

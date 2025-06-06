import sys


class Tee:
    """A class to write to multiple streams simultaneously."""

    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for stream in self.streams:
            stream.write(data)

    def flush(self):
        for stream in self.streams:
            stream.flush()

    def close(self):
        for stream in self.streams:
            # Only close if the stream has a close method and is not sys.stdout/sys.stderr
            if hasattr(stream, "close") and stream not in (sys.stdout, sys.stderr, sys.__stdout__, sys.__stderr__):
                try:
                    stream.close()
                except Exception:
                    pass


def print_yellow(text: str) -> None:
    """Prints a given text in yellow color to the console."""

    print(f"\033[93m{text}\033[0m")


def over_to(agent_name: str) -> str:
    """Prints a message indicating the next agent to speak."""

    print_yellow(f"Over to {agent_name}...")
    return agent_name

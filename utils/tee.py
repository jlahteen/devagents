import sys


class Tee:
    """A class that redirects stdout and stderr to multiple streams simultaneously."""

    def __init__(self, *streams):
        for s in streams:
            if not (
                hasattr(s, "write")
                and callable(s.write)
                and hasattr(s, "flush")
                and callable(s.flush)
                and hasattr(s, "close")
                and callable(s.close)
            ):
                raise TypeError(
                    f"A stream must have the write(), flush(), and close() methods. '{type(s)}' does not have at least one of these methods."
                )
        self.streams = streams
        # Redirect sys.stdout and sys.stderr to this Tee instance
        sys.stdout = self
        sys.stderr = self

    def write(self, data):
        for stream in self.streams:
            stream.write(data)

    def flush(self):
        for stream in self.streams:
            stream.flush()

    def close(self):
        for stream in self.streams:
            # Do not close the original sys.stdout/sys.stderr streams
            if stream not in (sys.__stdout__, sys.__stderr__):
                stream.close()
        # Restore sys.stdout and sys.stderr to their original values
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

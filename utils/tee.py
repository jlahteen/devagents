import sys


class Tee:
    """A class to write to multiple streams simultaneously."""

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
                raise TypeError(f"All streams must have write(data), flush(), and close() methods, got {type(s)}")
        self.streams = streams

    def write(self, data):
        for stream in self.streams:
            stream.write(data)

    def flush(self):
        for stream in self.streams:
            stream.flush()

    def close(self):
        for stream in self.streams:
            # Do not close sys.stdout/sys.stderr streams
            if stream not in (sys.__stdout__, sys.__stderr__):
                stream.close()

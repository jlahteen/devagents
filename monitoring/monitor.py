import abc


class TeeStreamBase(abc.ABC):
    """Abstract base class for Tee streams."""

    @abc.abstractmethod
    def write(self, data):
        """Writes data to the stream."""
        pass

    @abc.abstractmethod
    def flush(self):
        """Flushes the stream."""
        pass

    @abc.abstractmethod
    def close(self):
        """Closes the stream."""
        pass


class MonitorBase(TeeStreamBase):
    """Abstract base class for monitors."""

    @abc.abstractmethod
    def set_current_agent(self, current_agent):
        """Sets the current agent in the monitor."""
        pass

    @abc.abstractmethod
    def get_terminal_height_width(self, current_agent):
        """Returns the current terminal height and width as a tuple."""
        pass

import os
import platform
import subprocess
import sys
import threading
import time
from io import StringIO

# Unix-specific imports for PTY support (Linux only)
try:
    import pty
    import select
except ImportError:
    # Not available on Windows; _run_with_pty won't be called there anyway
    pass

from utils.misc import print_tool_error, print_tool_use

file_lock = threading.Lock()

# Define the required constants for timeouts, buffer sizes etc.
_DEFAULT_INACTIVITY_TIMEOUT = 420
_READ_CHUNK_SIZE = 8192
_SELECT_TIMEOUT = 0.5
_FINAL_READ_ATTEMPTS = 3
_FINAL_READ_TIMEOUT = 0.1
_SUBPROCESS_WAIT_TIMEOUT = 10
_SUBPROCESS_RETRY_SLEEP = 0.01
_SIGKILL = 9

# Define the constants for the standard Unix file descriptors
_STDIN_FILENO = 0
_STDOUT_FILENO = 1
_STDERR_FILENO = 2


def run_command(command: str) -> str:
    """
    Executes a shell command with a real-time streaming output. Returns error messages as strings, never raises
    exceptions.
    - On Linux: uses PTY for the best terminal emulation
    - On Windows: uses subprocess with line buffering (for development/testing purposes)
    """

    with file_lock:
        print_tool_use(command)

        system = platform.system().lower()
        if system == "linux":
            return _run_with_pty(command)
        else:
            return _run_with_subprocess(command)


def _format_error_result(error_msg: str, output_text: str) -> str:
    """Defines a helper to format error messages consistently."""

    print_tool_error(error_msg)
    return error_msg + ("\n" + output_text if output_text else "")


def _write_output(text: str, capture: StringIO) -> None:
    """Defines a helper to write to both stdout and capture."""

    sys.stdout.write(text)
    sys.stdout.flush()
    capture.write(text)


def _handle_command_result(command: str, timed_out: bool, exit_code: int, output_text: str) -> str:
    """Helper to handle command result and format an appropriate return message."""

    if timed_out:
        error_msg = f"run_command ERROR: Command '{command}' had no output for {_DEFAULT_INACTIVITY_TIMEOUT} seconds (it was likely waiting for user input)"
        return _format_error_result(error_msg, output_text)
    elif exit_code == 0:
        print()
        return output_text
    else:
        error_msg = f"run_command ERROR: Command '{command}' reported an error (code {exit_code})"
        return _format_error_result(error_msg, output_text)


def _handle_command_exception(command: str, e: Exception, output_capture: StringIO) -> str:
    """Helper to handle exceptions during command execution."""

    output_text = output_capture.getvalue()
    error_msg = f"run_command ERROR: Failed to run the command '{command}': {str(e)}"
    return _format_error_result(error_msg, output_text)


def _run_with_pty(command: str) -> str:
    """Executes a shell command using a pseudo-terminal (PTY) for the best terminal emulation on Linux."""

    output_capture = StringIO()

    try:
        # Create the master (our side) and slave (child process side) terminal FDs
        master_fd, slave_fd = pty.openpty()
    except Exception as e:
        error_msg = f"run_command ERROR: Failed to create PTY: {str(e)}"
        print_tool_error(error_msg)
        return error_msg

    try:
        # Create a child process to run the command
        pid = os.fork()
        if pid == 0:
            # Child process
            try:
                # Create a new session (detach from parent's terminal)
                os.setsid()
                # The child doesn't need master FD
                os.close(master_fd)

                # Redirect stdin to /dev/null to prevent interactive prompts
                devnull = os.open("/dev/null", os.O_RDONLY)
                os.dup2(devnull, _STDIN_FILENO)
                os.close(devnull)

                # Redirect stdout and stderr to the slave PTY
                os.dup2(slave_fd, _STDOUT_FILENO)
                os.dup2(slave_fd, _STDERR_FILENO)
                os.close(slave_fd)

                # Replace the child process with a shell running our command
                os.execvp("sh", ["sh", "-c", command])
            except Exception:
                os._exit(1)

        # The parent process continues here
        # The parent doesn't need the slave FD
        os.close(slave_fd)

        last_output_time = time.monotonic()
        timed_out = False

        try:
            while True:
                # Check the inactivity timeout
                if time.monotonic() - last_output_time > _DEFAULT_INACTIVITY_TIMEOUT:
                    timed_out = True
                    try:
                        os.kill(pid, _SIGKILL)
                    except OSError:
                        pass
                    break

                # Wait for data to be available on master_fd (with timeout)
                # select() returns when data is ready or timeout expires
                ready_list, _, _ = select.select([master_fd], [], [], _SELECT_TIMEOUT)

                if master_fd in ready_list:
                    try:
                        data = os.read(master_fd, _READ_CHUNK_SIZE)
                        if not data:
                            # EOF - child closed its stdout/stderr
                            break

                        text = data.decode("utf-8", errors="replace")
                        _write_output(text, output_capture)
                        last_output_time = time.monotonic()
                    except OSError:
                        # Error in reading - the child probably died
                        break

                # Check if the child process has exited (non-blocking)
                result = os.waitpid(pid, os.WNOHANG)
                if result[0] != 0:
                    # The child process has exited - drain any buffered output
                    for _ in range(_FINAL_READ_ATTEMPTS):
                        try:
                            ready_list, _, _ = select.select([master_fd], [], [], _FINAL_READ_TIMEOUT)
                            if ready_list:
                                data = os.read(master_fd, _READ_CHUNK_SIZE)
                                if data:
                                    text = data.decode("utf-8", errors="replace")
                                    _write_output(text, output_capture)
                                else:
                                    break
                            else:
                                # No more data available
                                break
                        except OSError:
                            break
                    break

        finally:
            os.close(master_fd)
            try:
                # Reap the zombie process and get the exit code
                _, status = os.waitpid(pid, 0)
                exit_code = os.WEXITSTATUS(status) if os.WIFEXITED(status) else 1
            except ChildProcessError:
                # Already reaped
                exit_code = 1

        output_text = output_capture.getvalue()

        return _handle_command_result(command, timed_out, exit_code, output_text)

    except Exception as e:
        return _handle_command_exception(command, e, output_capture)


def _run_with_subprocess(command: str) -> str:
    """Executes a shell command using a subprocess with line buffering for Windows."""

    output_capture = StringIO()

    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            encoding="utf-8",
            errors="replace",
        )

        last_activity = time.monotonic()
        timed_out = False

        def watchdog() -> None:
            nonlocal timed_out
            while process.poll() is None:
                time.sleep(1)
                if time.monotonic() - last_activity > _DEFAULT_INACTIVITY_TIMEOUT:
                    timed_out = True
                    process.kill()
                    break

        threading.Thread(target=watchdog, daemon=True).start()

        # Read line by line
        for line in iter(process.stdout.readline, ""):
            if not line:
                # Check if process is still running
                if process.poll() is None:
                    time.sleep(_SUBPROCESS_RETRY_SLEEP)
                    continue
                break
            last_activity = time.monotonic()
            print(line, end="", flush=True)
            output_capture.write(line)

        # Final drain
        remaining = process.stdout.read()
        if remaining:
            print(remaining, end="", flush=True)
            output_capture.write(remaining)

        process.wait(timeout=_SUBPROCESS_WAIT_TIMEOUT)
        process.stdout.close()

        output_text = output_capture.getvalue()
        return_code = process.returncode

        return _handle_command_result(command, timed_out, return_code, output_text)

    except Exception as e:
        return _handle_command_exception(command, e, output_capture)

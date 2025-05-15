import subprocess
import threading

file_lock = threading.Lock()


def run_command(command: str) -> str:
    """Runs a specified command and captures all output, including errors."""

    with file_lock:
        print(f"run_command: Running command '{command}'...")
        try:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                capture_output=True,
                text=True,
            )
            print(f"run_command OK: Command '{command}' was run successfully")
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"run_command ERROR: Command '{command}' reported an error")
            return (
                f"run_command ERROR: Command '{command}' reported an error:\n"
                f"STDOUT: {e.stdout}\n"
                f"STDERR: {e.stderr}"
            )
        except Exception as e:
            return f"run_command ERROR: Failed to run the command '{command}': {str(e)}"

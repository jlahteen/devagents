import subprocess
import sys
import threading
from io import StringIO

from utils.misc import Tee

file_lock = threading.Lock()


def run_command(command: str) -> str:
    """Runs a specified command, streams all output to the console, and returns the full output."""

    with file_lock:
        print(f"run_command: Running command '{command}'...")

        output = StringIO()
        tee = Tee(sys.stdout, output)

        try:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True,
                encoding="utf-8",
                errors="replace",
            )

            for line in iter(process.stdout.readline, ""):
                tee.write(line)
                tee.flush()

            return_code = process.wait()
            process.stdout.close()

            output_lines = output.getvalue()

            if return_code == 0:
                print(f"run_command OK: Command '{command}' was run successfully")
                return output_lines
            else:
                error_msg = f"run_command ERROR: Command '{command}' reported an error (code {return_code})"
                print(error_msg)
                return error_msg + "\n" + output_lines

        except Exception as e:
            error_msg = f"run_command ERROR: Failed to run the command '{command}': {str(e)}"
            print(error_msg)
            return error_msg

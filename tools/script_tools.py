import subprocess
import os


# Runs a specified script. Only Windows OS is currently supported.
def run_script(script_path: str) -> str:
    try:
        result = subprocess.run(
            ["cmd", "/c", script_path.replace("/", "\\")],
            check=True,
            capture_output=True,
            text=True,
        )
        print(f"run_script OK: Script '{script_path}' was run successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"run_script ERROR: Failed to run the script '{script_path}': {e.stderr}"
    except Exception as e:
        return f"run_script ERROR: Failed to run the script '{script_path}': {str(e)}"

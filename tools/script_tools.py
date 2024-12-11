import subprocess
import os


def run_script(script_path: str) -> str:
    """
    Runs a specified script.

    When running the script, the function sets the current directory corresponding to a location of the script.
    Note: Only Windows OS is currently supported.
    """
    try:
        original_dir = os.getcwd()

        # Extract the directory from the script path
        script_dir = os.path.dirname(script_path)
        script_file = os.path.basename(script_path)

        # Set cwd to None if there's no directory part
        cwd = script_dir if script_dir else None

        # Run the script
        result = subprocess.run(
            ["cmd", "/c", script_file.replace("/", "\\")],
            check=True,
            capture_output=True,
            text=True,
            cwd=cwd,
        )
        print(f"run_script OK: Script '{script_path}' was run successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"run_script ERROR: Failed to run the script '{script_path}': {e.stderr}"
    except Exception as e:
        return f"run_script ERROR: Failed to run the script '{script_path}': {str(e)}"
    finally:
        os.chdir(original_dir)

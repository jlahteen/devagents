import subprocess
import os
import tempfile


def run_script(script: str) -> str:
    """
    Runs a specified script.

    The function saves the specified script to a temp file of type *.bat and
    runs the temp file with the cmd /c option.

    Note: Only Windows OS is currently supported.
    """

    script_start = (script if len(script) <= 25 else script[:25] + "...").replace(
        "\n", " "
    )

    # Save the script to a temporary file
    with tempfile.NamedTemporaryFile(
        delete=False, mode="w", suffix=".bat"
    ) as temp_file:
        temp_file.write(script)
        temp_file_path = temp_file.name

    try:
        # Run the script from the temp file
        result = subprocess.run(
            ["cmd", "/c", temp_file_path],
            check=True,
            capture_output=True,
            text=True,
        )

        print(f"run_script OK: Script '{script_start}' was run successfully")
        return result.stdout
    except Exception as e:
        return f"run_script ERROR: Failed to run the script '{script_start}': {str(e)}"

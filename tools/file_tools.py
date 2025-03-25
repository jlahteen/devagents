import os
import threading

file_lock = threading.Lock()

def save_file(file_path: str, file_content: str) -> str:
    """
    Saves a file content to a file.

    If the file path contains a directory and it does not exist, the function creates it.
    """

    try:
        directory = os.path.dirname(file_path)
        # Allow only one thread to access the next section because of directory creation
        with file_lock:
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            with open(file_path, "w") as file:
                file.write(file_content)
                file.flush()
                os.fsync(file.fileno())
        print(f"save_file OK: Content was saved to '{file_path}'")
        return file_path
    except Exception as e:
        return f"save_file ERROR: An error occurred while saving content to the file '{file_path}': {e}"

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
        print(f"save_file OK: Content was saved to the file '{file_path}'")
        return file_path
    except Exception as e:
        return f"save_file ERROR: Failed to save the content to the file '{file_path}': {e}"


def read_file(file_path: str) -> str:
    """
    Reads the content of a file.

    If the file does not exist, the function returns an error message.
    """
    try:
        # Allow only one thread to access the file reading section
        with file_lock:
            if not os.path.exists(file_path):
                return f"read_file ERROR: The file '{file_path}' does not exist"
            with open(file_path, "r") as file:
                file_content = file.read()
        print(f"read_file OK: Content of the file '{file_path}' was read")
        return file_content
    except Exception as e:
        return f"read_file ERROR: Failed to read the file '{file_path}': {e}"


def enum_subdirs(dir_path: str) -> list:
    """
    Enumerates all subdirectories of a given directory.

    If the directory does not exist, the function returns an error message.
    """
    try:
        # Allow only one thread to access the directory listing section
        with file_lock:
            if not os.path.exists(dir_path):
                return f"enum_subdirs ERROR: The directory '{dir_path}' does not exist"
            subdirs = [d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))]
        print(f"enum_subdirs OK: Subdirectories of the directory '{dir_path}' were enumerated")
        return subdirs
    except Exception as e:
        return f"enum_subdirs ERROR: Failed to enumerate the subdirectories of '{dir_path}': {e}"


def enum_files(dir_path: str) -> list:
    """
    Enumerates all files of a given directory.

    If the directory does not exist, the function returns an error message.
    """
    try:
        # Allow only one thread to access the directory listing section
        with file_lock:
            if not os.path.exists(dir_path):
                return f"enum_files ERROR: The directory '{dir_path}' does not exist"
            files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
        print(f"enum_files OK: Files of the directory '{dir_path}' were enumerated")
        return files
    except Exception as e:
        return f"enum_files ERROR: Failed to enumerate the files of '{dir_path}': {e}"


def delete_file(file_path: str) -> str:
    """
    Deletes a file.

    If the file does not exist, the function returns an error message.
    """
    try:
        # Allow only one thread to access the file deletion section
        with file_lock:
            if not os.path.exists(file_path):
                return f"delete_file ERROR: The file '{file_path}' does not exist"
            os.remove(file_path)
        print(f"delete_file OK: The file '{file_path}' was deleted")
        return f"delete_file OK: The file '{file_path}' was deleted"
    except Exception as e:
        return f"delete_file ERROR: Failed to delete the file '{file_path}': {e}"

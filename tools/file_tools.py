import fnmatch
import os
import threading

from utils.misc import print_tool_error, print_tool_use

file_lock = threading.Lock()


def save_file(file_path: str, file_content: str) -> str:
    """
    Saves a file content to a file as UTF-8.

    If the file path contains a directory and it does not exist, the function creates it.
    """

    try:
        directory = os.path.dirname(file_path)
        # Allow only one thread to access the next section because of directory creation
        with file_lock:
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(file_content)
                file.flush()
                os.fsync(file.fileno())
        print_tool_use(f"save_file: '{file_path}'")
        return file_path
    except Exception as e:
        error_msg = f"save_file ERROR: Failed to save the content to the file '{file_path}': {e}"
        print_tool_error(error_msg)
        return error_msg


def read_file(file_path: str) -> str:
    """
    Reads the content of a file as UTF-8.

    If the file does not exist, the function returns an error message.
    """
    try:
        # Allow only one thread to access the file reading section
        with file_lock:
            if not os.path.exists(file_path):
                return f"read_file ERROR: The file '{file_path}' does not exist"
            with open(file_path, "r", encoding="utf-8") as file:
                file_content = file.read()
        print_tool_use(f"read_file: '{file_path}'")
        return file_content
    except Exception as e:
        error_msg = f"read_file ERROR: Failed to read the file '{file_path}': {e}"
        print_tool_error(error_msg)
        return error_msg


def read_previous_version(file_path: str) -> str:
    """
    Reads the previous (i.e. current) version of a file.

    If the file does not exist, returns a message indicating it's a new file with no previous version.
    """

    try:
        with file_lock:
            if not os.path.exists(file_path):
                return f"File '{file_path}' is new, no previous version exists."
            else:
                with open(file_path, "r", encoding="utf-8") as file:
                    result = file.read()

        print_tool_use(f"read_previous_version: '{file_path}'")
        return result
    except Exception as e:
        error_msg = f"read_previous_version ERROR: Failed to read the file '{file_path}': {e}"
        print_tool_error(error_msg)
        return error_msg


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
            subdirs = [
                d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d)) and d != ".devagents"
            ]
        print_tool_use(f"enum_subdirs: '{dir_path}'")
        return subdirs
    except Exception as e:
        error_msg = f"enum_subdirs ERROR: Failed to enumerate the subdirectories of '{dir_path}': {e}"
        print_tool_error(error_msg)
        return error_msg


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
        print_tool_use(f"enum_files: '{dir_path}'")
        return files
    except Exception as e:
        error_msg = f"enum_files ERROR: Failed to enumerate the files of '{dir_path}': {e}"
        print_tool_error(error_msg)
        return error_msg


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
        print_tool_use(f"delete_file: '{file_path}'")
        return f"delete_file OK: The file '{file_path}' was deleted"
    except Exception as e:
        error_msg = f"delete_file ERROR: Failed to delete the file '{file_path}': {e}"
        print_tool_error(error_msg)
        return error_msg


def search_in_files(dir_path: str, search_term: str, file_name_mask: str) -> list:
    """
    Recursively searches for files in a given directory and its subdirectories whose names match the file_name_mask.
    For each matching file, searches for the search_term (case-insensitive) in the file's contents.
    The .devagents directory is excluded from the search.

    If the directory does not exist, the function returns an error message.
    """

    try:
        if not os.path.exists(dir_path):
            return f"search_in_files ERROR: The directory '{dir_path}' does not exist"
        search_term_lower = search_term.lower()
        matching_files = []
        for root, dirs, files in os.walk(dir_path):
            if ".devagents" in dirs:
                dirs.remove(".devagents")
            for filename in files:
                if fnmatch.fnmatch(filename, file_name_mask):
                    file_path = os.path.join(root, filename)
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read().lower()
                            if search_term_lower in content:
                                matching_files.append(file_path)
                    except Exception:
                        pass
        result_text = f"search_in_files: Term '{search_term}' searched in files '{dir_path}/**/{file_name_mask}'"
        print_tool_use(result_text)
        return {"message": result_text, "result": matching_files}
    except Exception as e:
        error_msg = f"search_in_files ERROR: Failed to search for term '{search_term}' in files '{dir_path}/**/{file_name_mask}': {e}"
        print_tool_error(error_msg)
        return error_msg


def file_exists(file_path: str) -> str:
    """Checks if a file exists. Returns a message indicating the result."""

    try:
        exists = os.path.exists(file_path)
        if exists:
            result = f"File '{file_path}' does exist"
        else:
            result = f"File '{file_path}' does not exist"
        print_tool_use(f"file_exists: '{file_path}'")
        return result
    except Exception as e:
        result = f"Failed to check the existence of the file '{file_path}': {e}"
        print_tool_error(f"file_exists ERROR: {result}")
        return result

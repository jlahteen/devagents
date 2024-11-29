import os


# Saves a file content to a file path. If the file path contains a directory and it does not
# exist, the method creates it.
def save_file(file_path: str, file_content: str) -> str:
    try:
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        with open(file_path, "w") as file:
            file.write(file_content)
        print(f"save_file OK: Content was saved to '{file_path}'")
        return file_path
    except Exception as e:
        print(
            f"save_file ERROR: An error occurred while saving content to the file '{file_path}': {e}"
        )
        return ""

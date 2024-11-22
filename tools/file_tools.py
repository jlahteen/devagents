import os


# Saves code to a file. If the filename contains a directory and it does not
# exist, the method creates it.
def save_code_to_file(filename: str, code: str) -> str:
    try:
        directory = os.path.dirname(filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        with open(filename, "w") as file:
            file.write(code)
        print(f"Code was saved to {filename}")
        return filename
    except Exception as e:
        print(f"An error occurred while saving code to the file '{filename}': {e}")
        return ""

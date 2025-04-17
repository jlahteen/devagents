import os
import shutil


def copy_test_data(source_dir, dest_dir):
    """Copies a source directory to the destination directory."""

    # Ensure the source directory exists
    if not os.path.exists(source_dir):
        raise FileNotFoundError(f"Source directory '{source_dir}' does not exist")

    # Remove the destination directory if it exists
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    # Copy the source directory to the destination directory
    shutil.copytree(source_dir, dest_dir)


def create_test_run_dir(test_run_dir):
    """Creates a test run directory. If it exists, it will be removed and recreated."""

    # Remove the directory and recreate it
    if os.path.exists(test_run_dir):
        shutil.rmtree(test_run_dir)
    os.makedirs(test_run_dir)

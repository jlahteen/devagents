import os
import shutil

import pytest


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


@pytest.fixture
def setup_test(request):
    """Sets up a test by creating a test run directory with a proper test data."""

    base_dir = os.getcwd()
    test_module, test_name, test_data_dir = request.param
    test_run_dir = os.path.join(base_dir, "tests", "test_output", test_module, test_name)
    create_test_run_dir(test_run_dir)
    if test_data_dir:
        test_data_dir = os.path.join(base_dir, "tests", "test_data", test_data_dir)
        copy_test_data(test_data_dir, test_run_dir)
    os.chdir(test_run_dir)
    yield test_run_dir
    os.chdir(base_dir)


def assert_file_contains(file_path: str, expected_content: str):
    """Asserts that a file contains the expected content."""

    if not os.path.exists(file_path):
        raise AssertionError(f"File '{file_path}' does not exist")
    with open(file_path, "r", encoding="utf-8") as f:
        file_content = f.read()
    if expected_content not in file_content:
        raise AssertionError(f"File '{file_path}' does not contain expected content")

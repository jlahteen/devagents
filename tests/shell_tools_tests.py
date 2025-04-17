import os

import pytest

from tests.test_utils import copy_test_data
from tools.shell_tools import run_command


@pytest.mark.asyncio
async def test_dotnet_build__should_build():
    # Arrange
    base_dir = os.getcwd()
    test_data_dir = os.path.join(base_dir, "tests", "test_data", "hello_world_console_app")
    test_run_dir = os.path.join(base_dir, "tests", "test_output", "test_dotnet_build")
    copy_test_data(test_data_dir, test_run_dir)
    os.chdir(test_run_dir)

    # Act
    result = run_command("dotnet build")

    # Assert
    assert os.path.exists(os.path.join(test_run_dir, "bin\\Debug\\net8.0\\HelloWorld.dll"))
    assert os.path.exists(os.path.join(test_run_dir, "bin\\Debug\\net8.0\\HelloWorld.exe"))

    # Clean up
    os.chdir(base_dir)

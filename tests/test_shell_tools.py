import os

import pytest

from tests.test_utils import setup_test
from tools.shell_tools import run_command
from utils.misc import to_os_path


@pytest.mark.parametrize(
    "setup_test",
    [("shell_tools", "test_dotnet_build", "hello_world_cs_console_app")],
    indirect=True,
)
@pytest.mark.asyncio
async def test_dotnet_build__should_build(setup_test):
    # Arrange
    test_run_dir = setup_test

    # Act
    result = run_command("dotnet build")
    print(result)

    # Assert
    "Build succeeded." in result
    "0 Warning(s)" in result
    "0 Error(s)" in result
    assert os.path.exists(os.path.join(test_run_dir, to_os_path("bin\\Debug\\net8.0\\HelloWorld.dll")))
    assert os.path.exists(os.path.join(test_run_dir, to_os_path("bin\\Debug\\net8.0\\HelloWorld.exe")))

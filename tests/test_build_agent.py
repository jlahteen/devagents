import os

import pytest

from agents.build_agent import BuildAgent
from tests.test_utils import setup_test
from utils.config import Config
from utils.misc import to_os_path


@pytest.mark.parametrize(
    "setup_test",
    [("build_agent", "test_broken_build", "simple_cs_console_app_broken")],
    indirect=True,
)
@pytest.mark.asyncio
async def test_broken_build__should_fix(setup_test):
    # Arrange
    test_run_dir = setup_test
    build_agent = BuildAgent(config=Config(), monitor=None, on_error_callback=None)

    # Act
    await build_agent.run_inner_team(prompt="Fix the build.")

    # Assert
    assert os.path.exists(os.path.join(test_run_dir, to_os_path("bin\\Release\\net8.0\\FinnishSSNValidator.dll")))
    assert os.path.exists(os.path.join(test_run_dir, to_os_path("bin\\Release\\net8.0\\FinnishSSNValidator.exe")))

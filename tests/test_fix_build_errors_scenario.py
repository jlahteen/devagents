import os

import pytest
from autogen_agentchat.ui import Console

from config import Config
from scenarios.fix_build_errors.fix_build_errors_scenario import FixBuildErrorsScenario
from tests.test_utils import copy_test_data


@pytest.mark.asyncio
async def test_broken_build__should_fix():
    # Arrange
    base_dir = os.getcwd()
    test_data_dir = os.path.join(base_dir, "tests", "test_data", "simple_console_app_broken")
    test_run_dir = os.path.join(base_dir, "tests", "test_output\\fix_build_errors_scenario", "test_broken_build")
    copy_test_data(test_data_dir, test_run_dir)
    os.chdir(test_run_dir)
    scenario = FixBuildErrorsScenario(config=Config())

    # Act
    await scenario.run_scenario(prompt="Fix the build errors in the project.")

    # Assert
    assert os.path.exists(os.path.join(test_run_dir, "bin\\Debug\\net8.0\\FinnishSSNValidator.dll"))
    assert os.path.exists(os.path.join(test_run_dir, "bin\\Debug\\net8.0\\FinnishSSNValidator.exe"))

    # Clean up
    os.chdir(base_dir)

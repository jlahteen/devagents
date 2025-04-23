import os

import pytest

from config import Config
from scenarios.fix_build_errors.fix_build_errors_scenario import FixBuildErrorsScenario
from tests.test_utils import setup_test


@pytest.mark.parametrize(
    "setup_test",
    [("fix_build_errors_scenario", "test_broken_build", "simple_console_app_broken")],
    indirect=True,
)
@pytest.mark.asyncio
async def test_broken_build__should_fix(setup_test):
    # Arrange
    test_run_dir = setup_test
    scenario = FixBuildErrorsScenario(config=Config())

    # Act
    await scenario.run_scenario(prompt="Fix the build errors in the project.")

    # Assert
    assert os.path.exists(os.path.join(test_run_dir, "bin\\Debug\\net8.0\\FinnishSSNValidator.dll"))
    assert os.path.exists(os.path.join(test_run_dir, "bin\\Debug\\net8.0\\FinnishSSNValidator.exe"))

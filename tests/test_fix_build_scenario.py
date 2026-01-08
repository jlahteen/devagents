import os

import pytest

from workflows.fix_build.fix_build_scenario import FixBuildScenario
from tests.test_utils import setup_test
from utils.config import Config
from utils.misc import to_os_path


@pytest.mark.parametrize(
    "setup_test",
    [("fix_build_errors_scenario", "test_broken_build", "simple_cs_console_app_broken")],
    indirect=True,
)
@pytest.mark.asyncio
async def test_broken_build__should_fix(setup_test):
    # Arrange
    test_run_dir = setup_test
    scenario = FixBuildScenario()
    orchestrator_agent = scenario.create_orchestrator_agent(config=Config())

    # Act
    await orchestrator_agent.run_team(prompt="Fix the build errors in the project.")

    # Assert
    assert os.path.exists(os.path.join(test_run_dir, to_os_path("bin\\Debug\\net8.0\\FinnishSSNValidator.dll")))
    assert os.path.exists(os.path.join(test_run_dir, to_os_path("bin\\Debug\\net8.0\\FinnishSSNValidator.exe")))

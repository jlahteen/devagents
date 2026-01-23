import io
import sys
from contextlib import redirect_stdout

import pytest

from monitoring.console_monitor_ansi import ConsoleMonitorAnsi
from tests.test_utils import setup_test
from utils.config import Config
from utils.constants import TEST_AGENT_SUCCESSFUL
from utils.tee import Tee
from workflows.fix_tests.fix_tests_workflow import FixTestsWorkflow


@pytest.mark.parametrize(
    "setup_test",
    [("fix_tests_workflow", "test_failing_tests", "greeting_cs_console_app_with_failing_tests")],
    indirect=True,
)
@pytest.mark.asyncio
async def test_failing_tests__should_fix_and_pass(setup_test):
    # Arrange
    test_run_dir = setup_test
    console_output = io.StringIO()
    tee = Tee(sys.stdout, console_output)
    monitor = ConsoleMonitorAnsi()
    workflow = FixTestsWorkflow(config=Config(), monitor=monitor)

    # Act
    with redirect_stdout(tee):
        await workflow.run(prompt="Fix the build errors in the project.")
    output = console_output.getvalue()

    # Assert
    assert TEST_AGENT_SUCCESSFUL in output, "Expected text not found in console output."

import os
import textwrap

import pytest

from tests.test_utils import assert_file_contains, setup_test
from utils.config import Config
from utils.misc import to_os_path
from workflows.modify_app.modify_app_workflow import ModifyAppWorkflow

SKIP_TESTS = False

prompt_modify_hello_world_cs_console_app = textwrap.dedent(
    """
    Modify the Hello World C# console app to also display the current date and time below the greeting.
    Its output should look like this:
    Hello, World!
    Current date and time: {current_date_time}
    """
)


@pytest.mark.skipif(SKIP_TESTS, reason="Skipping test")
@pytest.mark.parametrize(
    "setup_test",
    [("modify_app_workflow", "modify_hello_world_cs", "hello_world_cs_console_app")],
    indirect=True,
)
@pytest.mark.asyncio
async def test_modify_hello_world_cs__displays_date_and_time(setup_test):
    # Arrange
    test_run_dir = setup_test
    workflow = ModifyAppWorkflow(config=Config())

    # Act
    await workflow.run(prompt=prompt_modify_hello_world_cs_console_app)
    output = os.popen(os.path.join(test_run_dir, to_os_path("bin\\Release\\net8.0\\HelloWorld.exe"))).read()
    print(output)

    # Assert
    assert "Hello, World!" in output
    assert "Current date and time:" in output

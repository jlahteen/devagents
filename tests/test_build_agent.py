import os

import pytest
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.ui import Console

from agents.build_agent import BuildAgent
from config import Config
from tests.test_utils import copy_test_data


@pytest.mark.asyncio
async def test_broken_build__should_fix():
    # Arrange
    base_dir = os.getcwd()
    test_data_dir = os.path.join(base_dir, "tests", "test_data", "simple_console_app_broken")
    test_run_dir = os.path.join(base_dir, "tests", "test_output\\build_agent", "test_broken_build")
    copy_test_data(test_data_dir, test_run_dir)
    os.chdir(test_run_dir)
    build_agent = BuildAgent(config=Config())

    # Act
    await Console(
        build_agent.on_messages_stream(
            [
                TextMessage(
                    content="Tell a joke. This has actually no meaning in this case.",
                    source="user",
                )
            ],
            cancellation_token=None,
        )
    )

    # Assert
    assert os.path.exists(os.path.join(test_run_dir, "bin\\Debug\\net8.0\\FinnishSSNValidator.dll"))
    assert os.path.exists(os.path.join(test_run_dir, "bin\\Debug\\net8.0\\FinnishSSNValidator.exe"))

    # Clean up
    os.chdir(base_dir)

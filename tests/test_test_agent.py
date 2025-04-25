import io
import sys
from contextlib import redirect_stdout

import pytest
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.ui import Console

from agents.test_agent import TestAgent
from config import Config
from constants import TEST_AGENT_SUCCESSFUL
from tests.test_utils import setup_test


class Tee:
    """A class to write to multiple streams simultaneously."""

    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for stream in self.streams:
            stream.write(data)

    def flush(self):
        for stream in self.streams:
            stream.flush()


@pytest.mark.parametrize(
    "setup_test",
    [("test_agent", "test_passing_tests", "greeting_cs_console_app")],
    indirect=True,
)
@pytest.mark.asyncio
async def test_passing_tests__should_pass(setup_test):
    # Arrange
    test_run_dir = setup_test
    test_agent = TestAgent(config=Config())
    console_output = io.StringIO()
    tee = Tee(sys.stdout, console_output)

    # Act
    with redirect_stdout(tee):
        await Console(
            test_agent.on_messages_stream(
                [
                    TextMessage(
                        content="Run and fix the tests.",
                        source="user",
                    )
                ],
                cancellation_token=None,
            )
        )
    output = console_output.getvalue()

    # Assert
    assert TEST_AGENT_SUCCESSFUL in output, "Expected text not found in console output."

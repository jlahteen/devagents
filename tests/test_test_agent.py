import io
import os
import sys
from contextlib import redirect_stdout

import pytest
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.ui import Console

from agents.test_agent import TestAgent
from tests.test_utils import setup_test
from utils.config import Config
from utils.constants import TEST_AGENT_SUCCESSFUL
from utils.tee import Tee

SKIP_TESTS = False


@pytest.mark.skipif(condition=SKIP_TESTS, reason="Skipping test")
@pytest.mark.parametrize(
    "setup_test",
    [("test_agent", "test_no_tests", "hello_world_cs_console_app")],
    indirect=True,
)
@pytest.mark.asyncio
async def test_no_tests__should_pass(setup_test):
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


@pytest.mark.skipif(condition=SKIP_TESTS, reason="Skipping test")
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


@pytest.mark.skipif(condition=SKIP_TESTS, reason="Skipping test")
@pytest.mark.parametrize(
    "setup_test",
    [
        (
            "test_agent",
            "test_fi_ssn_validator_lib_broken_tests_with_valid_test_data",
            "fi_ssn_validator_lib_broken_tests_with_valid_test_data",
        )
    ],
    indirect=True,
)
@pytest.mark.asyncio
async def test_fi_ssn_validator_lib_broken_tests_with_valid_test_data__should_fix_code_to_pass_tests(setup_test):
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
                        content="Fix the SSN Validator code to pass all the tests.",
                        source="user",
                    )
                ],
                cancellation_token=None,
            )
        )
    output = console_output.getvalue()

    # Assert
    unit_test_file = os.path.join(test_run_dir, "MyBase.FiSsnValidator.Tests", "ValidatorTests.cs")
    with open(unit_test_file, "r") as f:
        unit_test_code = f.read()
    assert '[DataRow("010101-123N", true)]' in unit_test_code, "Expected SSN result not fixed"
    assert '[DataRow("010101A123P", false)]' in unit_test_code, "Expected SSN result not fixed"
    assert '[DataRow("290202-1234", false)]' in unit_test_code, "Expected SSN result not fixed"
    assert '[DataRow("301299-123Y", false)]' in unit_test_code, "Expected SSN result not fixed"
    assert '[DataRow("150500-123A", false)]' in unit_test_code, "Expected SSN result not fixed"
    assert '[DataRow("151200A123B", false)]' in unit_test_code, "Expected SSN result not fixed"
    assert '[DataRow("060400-123C", false)]' in unit_test_code, "Expected SSN result not fixed"
    assert '[DataRow("290200-123D", false)]' in unit_test_code, "Expected SSN result not fixed"
    assert '[DataRow("290299-123E", false)]' in unit_test_code, "Expected SSN result not fixed"
    assert '[DataRow("100100A123F", false)]' in unit_test_code, "Expected SSN result not fixed"
    assert '[DataRow("010198A123G", false)]' in unit_test_code, "Expected SSN result not fixed"
    assert '[DataRow("010399A123H", false)]' in unit_test_code, "Expected SSN result not fixed"
    assert '[DataRow("010101-123M", false)]' in unit_test_code, "Expected SSN result not fixed"
    assert '[DataRow("010101-123Z", false)]' in unit_test_code, "Expected SSN result not fixed"
    assert '[DataRow("010101-123W", false)]' in unit_test_code, "Expected SSN result not fixed"
    assert '[DataRow("310232-123K", false)]' in unit_test_code, "Expected SSN result not fixed"
    assert '[DataRow("010101-123X", false)]' in unit_test_code, "Expected SSN result not fixed"
    assert '[DataRow("010101-123Y", false)]' in unit_test_code, "Expected SSN result not fixed"
    assert '[DataRow("010101-123Q", false)]' in unit_test_code, "Expected SSN result not fixed"
    assert '[DataRow("010101-123R", false)]' in unit_test_code, "Expected SSN result not fixed"
    assert '[DataRow("130593-935K", true)]' in unit_test_code, "Expected SSN result not fixed"
    assert '[DataRow("250757-969R", true)]' in unit_test_code, "Expected SSN result not fixed"
    assert '[DataRow("090222-987X", true)]' in unit_test_code, "Expected SSN result not fixed"
    assert '[DataRow("240332-943K", true)]' in unit_test_code, "Expected SSN result not fixed"
    assert '[DataRow("210268-931R", true)]' in unit_test_code, "Expected SSN result not fixed"
    assert '[DataRow("150776-947F", true)]' in unit_test_code, "Expected SSN result not fixed"
    assert TEST_AGENT_SUCCESSFUL in output, "Expected text not found in console output."

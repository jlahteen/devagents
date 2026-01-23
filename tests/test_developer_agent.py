import pytest

from agents.developer_agent import DeveloperAgent
from utils.config import Config
from utils.constants import WorkflowType


@pytest.mark.asyncio
async def test_generate_cs_console_hello_app__should_response_with_code():
    # Arrange
    developer_agent = DeveloperAgent(config=Config(), workflow_type=WorkflowType.NEW_CODE)

    # Act
    response = await developer_agent.run("Hello! Generate a C# console app that says 'Hello there!'.")
    print(response)

    # Assert
    assert "Console.Write" in response
    assert "Hello there!" in response

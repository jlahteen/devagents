import pytest
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken

from agents.developer_agent import DeveloperAgent
from config import Config


@pytest.mark.asyncio
async def test_generate_cs_console_hello_app_should_response_with_code():
    # Arrange
    developer_agent = DeveloperAgent(config=Config())
    cancellation_token = CancellationToken()

    # Act
    response = await developer_agent.on_messages(
        [
            TextMessage(
                content="Hello! Generate a C# console app that says 'Hello there!'.",
                source="user",
            )
        ],
        cancellation_token,
    )
    print(response)

    # Assert
    assert "Console.Write" in response.chat_message.content
    assert "Hello there!" in response.chat_message.content

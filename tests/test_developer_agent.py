from autogen_core import CancellationToken
from config import Config
from agents.developer_agent import DeveloperAgent
from autogen_agentchat.messages import TextMessage
import pytest


@pytest.mark.asyncio
async def test_developer_agent():
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

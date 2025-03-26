from autogen_core import CancellationToken
from config import Config
from autogen_core.models import ChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
import pytest


@pytest.mark.asyncio
async def test_config():
    # Arrange
    config = Config()
    model_client = ChatCompletionClient.load_component(config.model_client)
    assistant = AssistantAgent(
        name="assistant",
        system_message="You are a helpful assistant.",
        model_client=model_client,
    )
    cancellation_token = CancellationToken()
    # Act
    response = await assistant.on_messages(
        [TextMessage(content="Hello! Tell me a funny 'why' joke.", source="user")],
        cancellation_token,
    )
    print(response)
    # Assert
    assert "why" in response.chat_message.content.lower()

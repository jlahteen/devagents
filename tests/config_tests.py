import pytest
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from autogen_core.models import ChatCompletionClient

from config import Config


@pytest.mark.asyncio
async def test_init_agent_should_response_with_joke():
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

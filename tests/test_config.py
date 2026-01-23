import pytest

from agent_platform.agent_base import AgentBase
from utils.config import Config


@pytest.mark.asyncio
async def test_init_agent__should_response_with_joke():
    # Arrange
    config = Config()
    assistant = AgentBase(
        name="assistant",
        system_message="You are a helpful assistant.",
        config=config
    )

    # Act
    response = await assistant.run("Hello! Tell me a funny 'why' joke.")
    print(response)

    # Assert
    assert "why" in response.lower()

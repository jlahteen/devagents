import os
import textwrap

import pytest
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken

from agents.scaffold_agent import ScaffoldAgent
from config import Config
from tests.test_utils import setup_test

prompt = textwrap.dedent(
    """
    Create a "ChatGPT-like" React / TypeScript web app for the following use cases / requirements:
    - As a user I can write a request. The web app lists the request and gets the response by calling the backend of the app. In the backend, the app calls 3rd party service with a HTTP GET call domain/has?query=<request>
    - As a user I can see my requests and responses in the scrollable conversation area.
    
    Name the frontend project "my-chatgpt-frontend" and the backend project "my-chatgpt-backend".

    Use the latest React version and templates.

    Design the UI with fancy styles.
    """
)


@pytest.mark.parametrize(
    "setup_test",
    [("scaffold_agent", "test_scaffold_react_app", None)],
    indirect=True,
)
@pytest.mark.asyncio
async def test_scaffold_react_app__should_scaffold(setup_test):
    # Arrange
    test_run_dir = setup_test
    scaffold_agent = ScaffoldAgent(config=Config())
    cancellation_token = CancellationToken()

    # Act
    response = await scaffold_agent.on_messages(
        [
            TextMessage(
                content=prompt,
                source="user",
            )
        ],
        cancellation_token,
    )
    print(response)

    # Assert
    assert os.path.exists(os.path.join(test_run_dir, "my-chatgpt-frontend"))
    assert os.path.exists(os.path.join(test_run_dir, "my-chatgpt-backend"))
    assert os.path.exists(os.path.join(test_run_dir, "my-chatgpt-frontend", "node_modules"))
    assert os.path.exists(os.path.join(test_run_dir, "my-chatgpt-frontend", "src"))
    assert os.path.exists(os.path.join(test_run_dir, "my-chatgpt-frontend", "public"))

from autogen_core import CancellationToken
from config import Config
from agents.scaffold_agent import ScaffoldAgent
from autogen_agentchat.messages import TextMessage
import pytest
import textwrap
import os
import shutil

prompt = textwrap.dedent(
    """
    Create a "ChatGPT-like" React / TypeScript web app for the following use cases / requirements:
    - As a user I can write a request. The web app lists the request and gets the response by calling the backend of the app. In the backend, the app calls 3rd party service with a HTTP GET call domain/has?query=<request>
    - As a user I can see my requests and responses in the scrollable conversation area.
    
    Name the frontend project "my-chatgpt-frontend" and the backend project "my-chatgpt-backend".

    In this phase, you can mock the backend service.

    Use the latest React version and templates.

    Design the UI with fancy styles.
    """
)


@pytest.mark.asyncio
async def test_scaffold_agent():
    # Arrange

    # Set the test directory relative to the current working directory
    base_dir = os.getcwd()
    test_dir = os.path.join(base_dir, "output", "scaffold_test")

    # Remove the directory and recreate it
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)

    # Set the current directory to test_dir
    os.chdir(test_dir)
    print(f"Current working directory: {os.getcwd()}")
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
    assert os.path.exists(os.path.join(test_dir, "my-chatgpt-frontend"))
    assert os.path.exists(os.path.join(test_dir, "my-chatgpt-backend"))
    assert os.path.exists(os.path.join(test_dir, "my-chatgpt-frontend", "node_modules"))
    assert os.path.exists(os.path.join(test_dir, "my-chatgpt-frontend", "src"))
    assert os.path.exists(os.path.join(test_dir, "my-chatgpt-frontend", "public"))

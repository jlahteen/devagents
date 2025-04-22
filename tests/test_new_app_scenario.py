import os
import textwrap

import pytest

from config import Config
from scenarios.new_app.new_app_scenario import NewAppScenario
from tests.test_utils import create_test_run_dir

prompt = textwrap.dedent(
    """
    Write a C# console app that writes a random greeting to the console.
    
    Use .NET 8.
    
    The app should have a UI layer and a backend layer. The UI should get the greeting message from the backend and display it to the user.
    
    Create a new solution with two projects as follows:
    - MyGreetingApp.sln
    - MyGreetingApp.UI
    - MyGreetingApp.Backend
    
    The backend should have 20 different greeting and the should return randomly one of them
    """
)


@pytest.mark.asyncio
async def test_generate_cs_two_layer_greeting_app__creates_app():
    # Arrange
    base_dir = os.getcwd()
    test_run_dir = os.path.join(
        base_dir, "tests", "test_output\\new_app_scenario", "test_generate_cs_two_layer_greeting_app"
    )
    create_test_run_dir(test_run_dir)
    os.chdir(test_run_dir)
    scenario = NewAppScenario(config=Config())

    # Act
    await scenario.run_scenario(prompt=prompt)

    # Assert
    assert os.path.exists(os.path.join(test_run_dir, "MyGreetingApp.UI\\bin\\Debug\\net8.0\\MyGreetingApp.UI.dll"))
    assert os.path.exists(os.path.join(test_run_dir, "MyGreetingApp.UI\\bin\\Debug\\net8.0\\MyGreetingApp.UI.exe"))
    assert os.path.exists(
        os.path.join(test_run_dir, "MyGreetingApp.Backend\\bin\\Debug\\net8.0\\MyGreetingApp.Backend.dll")
    )

    # Clean up
    os.chdir(base_dir)

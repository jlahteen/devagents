import os
import textwrap

import pytest

from tests.test_utils import assert_file_contains, setup_test
from utils.config import Config
from workflows.new_architecture.new_architecture_workflow import NewArchitectureWorkflow


@pytest.mark.parametrize(
    "setup_test",
    [("new_architecture_workflow", "test_simple_todo_app", None)],
    indirect=True,
)
@pytest.mark.asyncio
async def test_simple_todo_app__should_create_architecture(setup_test):

    # Arrange
    test_run_dir = setup_test
    specs_content = textwrap.dedent(
        """
        # Specifications: Simple Todo App

        ## Overview
        A web-based application for managing personal todo lists.

        ## Features
        1. User authentication (login/logout)
        2. Create, edit, and delete todos
        3. Mark todos as complete/incomplete
        4. Filter todos by status (all, active, completed)
        5. Persistent storage

        ## Technical Requirements
        - Modern web frontend (React preferred)
        - RESTful API backend
        - Database for data persistence
        - User authentication and session management
        - Do not use Docker
        - Use Azure SQL Database as a DB

        ## Success Criteria
        - Users can manage their todos without data loss
        - Responsive design works on mobile and desktop
        - Fast page loads (< 2 seconds)
        """
    ).strip()
    specs_path = os.path.join(test_run_dir, "specs.md")
    with open(specs_path, "w", encoding="utf-8") as f:
        f.write(specs_content)
    workflow = NewArchitectureWorkflow(config=Config())

    # Act
    await workflow.run(prompt="create architecture from ./specs.md")

    # Assert
    architecture_path = os.path.join(test_run_dir, "specs-architecture.md")
    assert os.path.exists(architecture_path), "specs-architecture.md should be created next to specs.md"
    assert_file_contains(architecture_path, "## Overview")
    assert_file_contains(architecture_path, "## Components")
    assert_file_contains(architecture_path, "## Data Models")
    assert_file_contains(architecture_path, "## Authentication Mechanisms")
    assert_file_contains(architecture_path, "## Deployment Architecture")
    assert_file_contains(architecture_path, "## Architecture Diagrams")


@pytest.mark.parametrize(
    "setup_test",
    [("new_architecture_workflow", "test_react_digital_clock", None)],
    indirect=True,
)
@pytest.mark.asyncio
async def test_react_digital_clock__should_create_architecture(setup_test):

    # Arrange
    test_run_dir = setup_test
    specs_content = textwrap.dedent(
        """
        # Specifications: React Digital Clock

        ## Overview
        A simple React application that displays the current time as a digital clock with large digits.

        ## Features
        1. Display current time in HH:MM:SS format
        2. Auto-update every second
        3. Large, readable digital display
        4. Clean, modern UI
        5. Responsive design

        ## Technical Requirements
        - React 18+ with functional components and hooks
        - Use useState and useEffect for time management
        - CSS for styling the digital clock display
        - No external time libraries needed (use JavaScript Date)
        - Single page application (no routing needed)
        - Vite as build tool

        ## UI Requirements
        - Large digital font for time display (at least 48px)
        - Dark background with bright text for contrast
        - Center the clock on the page

        ## Success Criteria
        - Clock updates every second accurately
        - No performance issues or memory leaks
        - Works on desktop and mobile browsers
        - Clean, professional appearance
        """
    ).strip()
    specs_path = os.path.join(test_run_dir, "specs.md")
    with open(specs_path, "w", encoding="utf-8") as f:
        f.write(specs_content)
    workflow = NewArchitectureWorkflow(config=Config())

    # Act
    await workflow.run(prompt="create architecture from ./specs.md")

    # Assert
    architecture_path = os.path.join(test_run_dir, "specs-architecture.md")
    assert os.path.exists(architecture_path), "specs-architecture.md should be created next to specs.md"
    assert_file_contains(architecture_path, "## Overview")
    assert_file_contains(architecture_path, "## Components")
    assert_file_contains(architecture_path, "## Deployment Architecture")
    assert_file_contains(architecture_path, "## Architecture Diagrams")

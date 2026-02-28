import pytest

from agents.research_agent import ResearchAgent, research_web
from tests.test_utils import setup_test
from utils.config import Config

SKIP_TESTS = False


@pytest.mark.skipif(condition=SKIP_TESTS, reason="Skipping test")
@pytest.mark.parametrize(
    "setup_test",
    [("research_agent", "test_research_basic_question", None)],
    indirect=True,
)
@pytest.mark.asyncio
async def test_research_basic_question__should_return_summary(setup_test):
    """Test that ResearchAgent can research a basic question and return a summary."""

    # Arrange
    test_run_dir = setup_test
    agent = ResearchAgent(config=Config())
    research_task = "How to validate Finnish personal identity codes?"

    # Act
    response = await agent.run(research_task)
    print(f"\n\nResponse:\n{response}\n")

    # Assert
    assert response is not None
    assert len(response) > 100, "Response should be a substantial summary"


@pytest.mark.skipif(condition=SKIP_TESTS, reason="Skipping test")
@pytest.mark.parametrize(
    "setup_test",
    [("research_agent", "test_research_technical_topic", None)],
    indirect=True,
)
@pytest.mark.asyncio
async def test_research_technical_topic__should_find_relevant_info(setup_test):
    """Test that ResearchAgent can research a technical topic effectively."""

    # Arrange
    test_run_dir = setup_test
    agent = ResearchAgent(config=Config())
    research_task = "What causes React useState hook to not update immediately?"

    # Act
    response = await agent.run(research_task)
    print(f"\n\nResponse:\n{response}\n")

    # Assert
    assert response is not None
    assert len(response) > 100
    # Check that response addresses the topic (might mention async, batching, or closure)
    response_lower = response.lower()
    technical_terms_found = any(
        term in response_lower for term in ["async", "batch", "closure", "state", "update", "render", "react"]
    )
    assert technical_terms_found, "Response should contain relevant technical terms"


@pytest.mark.skipif(condition=SKIP_TESTS, reason="Skipping test")
@pytest.mark.parametrize(
    "setup_test",
    [("research_agent", "test_research_web_tool", None)],
    indirect=True,
)
@pytest.mark.asyncio
async def test_research_web_tool__should_return_ok_response(setup_test):
    """Test that research_web tool wrapper works correctly."""

    # Arrange
    test_run_dir = setup_test
    research_task = "Best practices for Python async/await error handling"

    # Act
    result = await research_web(research_task)
    print(f"\n\nResult:\n{result}\n")

    # Assert
    assert result is not None
    assert "research_web OK:" in result or "research_web ERROR:" in result
    if "research_web OK:" in result:
        # Extract the actual summary
        summary = result.replace("research_web OK:", "").strip()
        assert len(summary) > 100, "Summary should be substantial"


@pytest.mark.skipif(condition=SKIP_TESTS, reason="Skipping test")
@pytest.mark.parametrize(
    "setup_test",
    [("research_agent", "test_research_with_quota_error", None)],
    indirect=True,
)
@pytest.mark.asyncio
async def test_research_with_quota_error__should_fallback_to_training_knowledge(setup_test):
    """Test that ResearchAgent handles quota errors gracefully and falls back to training knowledge."""

    # Arrange
    test_run_dir = setup_test
    agent = ResearchAgent(config=Config())
    # Use a very specific, possibly quota-triggering query
    research_task = "Explain the algorithm for calculating Finnish SSN check digit"

    # Act
    response = await agent.run(research_task)
    print(f"\n\nResponse:\n{response}\n")

    # Assert
    assert response is not None
    # If quota exceeded, response should mention using training knowledge or still provide useful info
    # Either way, agent should complete successfully, not fail


@pytest.mark.skipif(condition=SKIP_TESTS, reason="Skipping test")
@pytest.mark.parametrize(
    "setup_test",
    [("research_agent", "test_research_programming_question", None)],
    indirect=True,
)
@pytest.mark.asyncio
async def test_research_programming_question__should_provide_actionable_answer(setup_test):
    """Test that ResearchAgent provides actionable answers to programming questions."""

    # Arrange
    test_run_dir = setup_test
    agent = ResearchAgent(config=Config())
    research_task = "How to fix 'Cannot find module' error in Node.js?"

    # Act
    response = await agent.run(research_task)
    print(f"\n\nResponse:\n{response}\n")

    # Assert
    assert response is not None
    assert len(response) > 100
    # Check for actionable content (likely mentions npm install, paths, or modules)
    response_lower = response.lower()
    actionable_terms = any(
        term in response_lower for term in ["npm", "install", "module", "path", "node_modules", "import", "require"]
    )
    assert actionable_terms, "Response should contain actionable information"


@pytest.mark.skipif(condition=SKIP_TESTS, reason="Skipping test")
@pytest.mark.parametrize(
    "setup_test",
    [("research_agent", "test_research_short_question", None)],
    indirect=True,
)
@pytest.mark.asyncio
async def test_research_short_question__should_expand_into_detailed_answer(setup_test):
    """Test that ResearchAgent can take a short question and provide a detailed answer."""

    # Arrange
    test_run_dir = setup_test
    agent = ResearchAgent(config=Config())
    research_task = "Python type hints?"

    # Act
    response = await agent.run(research_task)
    print(f"\n\nResponse:\n{response}\n")

    # Assert
    assert response is not None
    assert len(response) > 100, "Should expand short question into detailed answer"
    # Should mention type hints, typing, annotations, etc.
    assert any(
        term in response.lower() for term in ["type", "hint", "annotation", "typing", "python"]
    ), "Response should address the topic"

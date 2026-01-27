import pytest

from tests.test_utils import setup_test
from tools.web_tools import google_search, load_page

SKIP_TESTS = False


@pytest.mark.skipif(condition=SKIP_TESTS, reason="Skipping test")
@pytest.mark.parametrize(
    "setup_test",
    [("web_tools", "test_google_search", None)],
    indirect=True,
)
@pytest.mark.asyncio
async def test_google_search__should_return_results(setup_test):
    # Arrange
    test_run_dir = setup_test

    # Act
    results = google_search("juha lähteenmäki linkedIn tieto")

    # Assert
    assert (
        results[0]["link"] == "https://fi.linkedin.com/in/juhalahteenmaki"
    ), "Expected link not found in search results."


@pytest.mark.skipif(condition=SKIP_TESTS, reason="Skipping test")
@pytest.mark.parametrize(
    "setup_test",
    [("web_tools", "test_load_page", None)],
    indirect=True,
)
@pytest.mark.asyncio
async def test_load_page__should_return_page_text(setup_test):
    # Arrange
    test_run_dir = setup_test

    # Act
    page_text = load_page("https://github.com/jlahteen/juhta.net")

    # Assert
    assert (
        "Juhta.NET is an open-source, general-purpose application framework" in page_text
    ), "Expected text not found in page text."

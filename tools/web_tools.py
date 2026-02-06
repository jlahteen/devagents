import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build

from utils.config import Config
from utils.misc import print_tool_error, print_tool_use


def google_search(query: str):
    """
    Performs a Google Custom Search and return simplified results.

    If the API key or CSE ID is not available, the message "Google searches are not available" will be returned.
    """

    try:
        config = Config()
        api_key = getattr(config.google_search, "api_key", "")
        cse_id = getattr(config.google_search, "cse_id", "")
        if not api_key or not cse_id:
            error_msg = "Google searches are not available, you are on your training knowledge, sorry."
            print_tool_error(f"google_search ERROR: {error_msg}")
            return error_msg
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=query, cx=cse_id, gl="fi").execute()
        simplified_results = [
            {"title": item.get("title"), "link": item.get("link"), "snippet": item.get("snippet")}
            for item in res.get("items", [])
        ]
        print_tool_use(f"google_search: Found {len(simplified_results)} results for query '{query}'")
        return simplified_results
    except Exception as e:
        error_msg = f"google_search ERROR: Failed to search for '{query}': {e}"
        print_tool_error(error_msg)
        return error_msg


def load_page(url: str) -> str:
    """
    Loads a specifed web page and return its text content from the HTML body.
    """

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        body = soup.body
        content = ""
        if body:
            content = body.get_text(separator="\n", strip=True)
        print_tool_use(f"load_page: Page loaded from '{url}' ({len(content)} characters)")
        return content
    except Exception as e:
        error_msg = f"load_page ERROR: Failed to load page from '{url}': {e}"
        print_tool_error(error_msg)
        return error_msg

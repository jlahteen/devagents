from urllib.parse import urlparse, urlunparse

import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from utils.config import Config
from utils.misc import print_tool_error, print_tool_use

# Cache for loaded pages (URL without fragment -> content)
_page_cache: dict[str, str] = {}


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
    except HttpError as e:
        # Check for quota/rate limit errors using actual HTTP status code
        if e.resp.status == 429:
            error_msg = "google_search ERROR: Quota exceeded for Google Custom Search API. Please use your training knowledge instead."
        else:
            error_msg = f"google_search ERROR: Failed to search for '{query}' (HTTP {e.resp.status}): {e}"
        print_tool_error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"google_search ERROR: Failed to search for '{query}': {e}"
        print_tool_error(error_msg)
        return error_msg


def load_page(url: str) -> str:
    """
    Loads a specified web page and returns its text content from the HTML body.

    Note: URL fragments (the part after #) are client-side only and ignored by the server.
    This function strips fragments before loading, so these URLs return the same content:
    - https://example.com/page
    - https://example.com/page#section1
    - https://example.com/page#section2

    Pages are cached to avoid redundant requests.
    """

    try:
        # Strip the URL fragment since it's client-side only
        parsed = urlparse(url)
        base_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, parsed.query, ""))

        # Check the cache first
        if base_url in _page_cache:
            cached_content = _page_cache[base_url]
            print_tool_use(f"load_page: '{base_url}' ({len(cached_content)} chars) (cached)")
            return cached_content

        # Fetch the page
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        body = soup.body
        content = ""
        if body:
            content = body.get_text(separator="\n", strip=True)

        # Cache the result
        _page_cache[base_url] = content

        print_tool_use(f"load_page: '{base_url}' ({len(content)} chars)")
        return content
    except requests.HTTPError as e:
        # HTTP error with status code
        status_code = e.response.status_code if e.response else "unknown"
        error_msg = f"load_page ERROR: Failed to load page from '{url}' (HTTP {status_code}): {e}"
        print_tool_error(error_msg)
        return error_msg
    except requests.RequestException as e:
        # Other request errors (timeout, connection error, etc.)
        error_msg = f"load_page ERROR: Failed to load page from '{url}': {e}"
        print_tool_error(error_msg)
        return error_msg
    except Exception as e:
        # All other errors
        error_msg = f"load_page ERROR: Failed to load page from '{url}': {e}"
        print_tool_error(error_msg)
        return error_msg

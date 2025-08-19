import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build

from utils.config import Config


def google_search(query: str):
    """
    Performs a Google Custom Search and return simplified results.

    If the API key or CSE ID is not available, a message "Google searches are not available" will be returned.
    """

    config = Config()
    api_key = getattr(config.google_search, "api_key", "")
    cse_id = getattr(config.google_search, "cse_id", "")
    if not api_key or not cse_id:
        return "Google searches are not available, you are on your training knowledge, sorry."
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=query, cx=cse_id, gl="fi").execute()
    simplified_results = [
        {"title": item.get("title"), "link": item.get("link"), "snippet": item.get("snippet")}
        for item in res.get("items", [])
    ]
    return simplified_results


def load_page(url: str) -> str:
    """
    Loads a specifed web page and return its text content from the HTML body.
    """

    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    body = soup.body
    if body:
        return body.get_text(separator="\n", strip=True)
    return ""

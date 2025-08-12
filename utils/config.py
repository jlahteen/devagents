import os

from dotenv import load_dotenv


class GoogleSearchConfig:
    """A class for Google Search configuration."""

    def __init__(self, api_key: str, cse_id: str):
        self.api_key = api_key
        self.cse_id = cse_id


class Config:
    """A class for configuration settings."""

    def __init__(self):
        load_dotenv()
        self.max_turns = int(os.getenv("MAX_TURNS"))
        self.model_client = {
            "provider": "AzureOpenAIChatCompletionClient",
            "config": {
                "model": os.getenv("AZURE_MODEL"),
                "azure_endpoint": os.getenv("AZURE_ENDPOINT"),
                "azure_deployment": os.getenv("AZURE_DEPLOYMENT"),
                "api_version": os.getenv("AZURE_API_VERSION"),
                "api_key": os.getenv("AZURE_API_KEY"),
            },
        }
        self.google_search = GoogleSearchConfig(
            api_key=os.getenv("GOOGLE_API_KEY"),
            cse_id=os.getenv("GOOGLE_CSE_ID"),
        )

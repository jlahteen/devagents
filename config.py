import os

from dotenv import load_dotenv


class Config:
    """A class for configuration settings."""

    def __init__(self):
        load_dotenv()
        self.max_turns = int(os.getenv("MAX_TURNS"))
        self.model_client = {
            "provider": "AzureOpenAIChatCompletionClient",
            "config": {
                "model": os.getenv("MODEL"),
                "azure_endpoint": os.getenv("AZURE_ENDPOINT"),
                "azure_deployment": os.getenv("AZURE_DEPLOYMENT"),
                "api_version": os.getenv("API_VERSION"),
                "api_key": os.getenv("API_KEY"),
            },
        }

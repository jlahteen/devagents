import os


# A class for configuration.
class Config:
    def __init__(self):
        self.max_rounds = 20
        self.llm_config = {
            "config_list": [
                {
                    "model": os.getenv("AZURE_GPT_DEPLOYMENT_NAME"),
                    "api_type": "azure",
                    "api_key": os.getenv("AZURE_OPENAI_KEY"),
                    "base_url": os.getenv("AZURE_OPENAI_URL"),
                    "api_version": "2024-05-01-preview",
                }
            ]
        }

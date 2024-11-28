import os
import textwrap


# Class for centralized configuration management
class Config:
    def __init__(self):
        self.max_rounds = 12
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
        self.developer_agent_system_message = textwrap.dedent(
            """
            You are a professional C# developer, known for reusable and maintainable code.
            You write almost bugless code which is highly appreciated among other developers.
            Add XML documentation for all essential places such as classes and methods.
            Add also step-by-step comments to internal implementations in methods.
            When you generate code, add the file name information for each file you generate.
            Include a directory to the file names if a directory is mentioned in the request.
            If there is no directory specified in the request, use the directory "output".
            You should improve the quality of your code based on the feedback from the reviewer.
            """
        )

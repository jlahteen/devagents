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
            Include a possible directory to the file names if a directort is mentioned in the request.
            If there is no directory specified in the request, use the directory "output".
            You should improve the quality of your code based on the feedback from the reviewer.
            """
        )

        self.reviewer_agent_system_message = textwrap.dedent(
            """
            You are a very experienced software architect, specialized in .NET/C#, You set the standards for the quality C# code.
            Your task is to review the code written by developer.
            If you approve the code, which means there are no mandatory issues to be fixed, just say 'CODE APPROVED' without any other content.
            if you do not approve the code, you should give constructive feedback and comments on how to make the code better.
            """
        )

        self.writer_agent_system_message = textwrap.dedent(
            """
            You get a conversation between a developer and a reviewer.
            When your turn comes, the reviewer has approved the code written by the developer.
            Your task is to save the APPROVED version of the code blocks to the files specified in the conversation.
            Note that the file names may include a directory part which must be followed.
            You use the _save_file_executor agent to save files.
            In the end, say TERMINATE.
            """
        )

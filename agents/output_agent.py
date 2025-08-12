import textwrap

from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import ChatCompletionClient

from tools.file_tools import save_file
from utils.config import Config


class OutputAgent(AssistantAgent):
    """
    An agent that saves all generated files.
    """

    _system_message = textwrap.dedent(
        """
        You are an agent that saves all the generated files.
        
        Your task is to save all files, both changed and unchanged, in the conversation. Save the
        files corresponding to their relative file paths in the current directory.

        Use the save_file tool to save files.
        """
    )

    def __init__(self, config: Config):
        super().__init__(
            name="output_agent",
            system_message=self._system_message,
            model_client=ChatCompletionClient.load_component(config.model_client),
            tools=[save_file],
        )

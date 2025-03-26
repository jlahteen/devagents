import re
from config import Config
from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import ChatCompletionClient


class OrchestratorAgentBase(AssistantAgent):
    """A base class for orchestrator agents."""

    def __init__(
        self,
        name,
        system_message,
        config: Config,
    ):
        super().__init__(
            name=name,
            system_message=system_message,
            model_client=ChatCompletionClient.load_component(config.model_client),
        )
        self._config = config

    def _is_code_approved(self, message):
        """Checks whether the code is approved in the given message."""
        
        # Use a regex to match 'CODE APPROVED' surrounded by any special characters
        pattern = r"[^a-zA-Z0-9]*CODE\sAPPROVED[^a-zA-Z0-9]*"

        # Split the message into lines and get the last line
        last_line = message.strip().split("\n")[-1]

        # Check the pattern against the last line
        return bool(re.fullmatch(pattern, last_line))

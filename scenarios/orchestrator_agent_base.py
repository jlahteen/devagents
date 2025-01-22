import re
from config import Config
from autogen import ConversableAgent


class OrchestratorAgentBase(ConversableAgent):
    """A base class for orchestrators."""

    def __init__(
        self,
        name,
        system_message,
        config: Config,
    ):
        super().__init__(
            llm_config=config.llm_config, name=name, system_message=system_message
        )
        self._code_execution_config = False
        self._human_input = "NEVER"
        self._config = config

    def _is_code_approved(self, message):
        # Use a regex to match 'CODE APPROVED' surrounded by any special characters
        pattern = r"[^a-zA-Z0-9]*CODE\sAPPROVED[^a-zA-Z0-9]*"

        # Split the message into lines and get the last line
        last_line = message.strip().split("\n")[-1]

        # Check the pattern against the last line
        return bool(re.fullmatch(pattern, last_line))

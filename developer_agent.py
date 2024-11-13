from config import Config
from autogen import ConversableAgent


class DeveloperAgent(ConversableAgent):
    def __init__(self, config: Config):
        super().__init__(
            name="developer_agent",
            system_message=config.developer_agent_system_message,
            llm_config=config.llm_config,
        )
        self._code_execution_config = False
        self._human_input = "NEVER"

import textwrap
from config import Config
from autogen import UserProxyAgent, ConversableAgent, GroupChat, GroupChatManager
from scenarios.orchestrator_agent_base import OrchestratorAgentBase


class OrchestratorAgent(OrchestratorAgentBase):
    """An orchestrator to run a NewApp scenario."""

    _system_message = textwrap.dedent(
        """
        You are an orchestrator agent that manages the DevAgents team consisting of AI agents.
        """
    )

    def __init__(
        self,
        config: Config,
        scaffold_agent,
        developer_agent,
        reviewer_agent,
        output_agent,
    ):
        super().__init__(
            name="orchestrator_agent",
            system_message=self._system_message,
            config=config,
        )
        self._scaffold_agent = scaffold_agent
        self._developer_agent = developer_agent
        self._reviewer_agent = reviewer_agent
        self._output_agent = output_agent

    def select_next_speaker(self, last_speaker, groupchat):
        if last_speaker is self._user_proxy_agent:
            return self._scaffold_agent
        elif last_speaker is self._scaffold_agent:
            return self._developer_agent
        elif last_speaker is self._developer_agent:
            return self._reviewer_agent
        elif last_speaker is self._reviewer_agent:
            if self._is_code_approved(groupchat.messages[-1]["content"]):
                return self._output_agent
            else:
                return self._developer_agent
        else:
            return None

    def start_chat(self, coding_request):
        # Create a user proxy agent
        self._user_proxy_agent = UserProxyAgent(
            "user_proxy_agent", human_input_mode="NEVER", code_execution_config=False
        )
        self.groupchat = GroupChat(
            agents=[
                self._user_proxy_agent,
                self._scaffold_agent,
                self._developer_agent,
                self._reviewer_agent,
                self._output_agent,
            ],
            speaker_selection_method=self.select_next_speaker,
            messages=[],
            max_round=self._config.max_rounds,
        )
        self.manager = GroupChatManager(
            groupchat=self.groupchat, llm_config=self._config.llm_config
        )
        chat_result = self._user_proxy_agent.initiate_chat(
            self.manager, message=coding_request
        )
        return chat_result

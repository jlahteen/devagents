import textwrap
from typing import Sequence
from config import Config
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from scenarios.orchestrator_agent_base import OrchestratorAgentBase
from autogen_agentchat.ui import Console
from autogen_agentchat.messages import AgentEvent, ChatMessage


class NewCodeOrchestratorAgent(OrchestratorAgentBase):
    """An orchestrator agent to run a NewCode scenario."""

    _system_message = textwrap.dedent(
        """
        You are an orchestrator agent that manages the AI agents team to complete a coding task.
        """
    )

    def __init__(
        self,
        config: Config,
        developer_agent,
        reviewer_agent,
        output_agent,
    ):
        super().__init__(
            name="orchestrator_agent",
            system_message=self._system_message,
            config=config,
        )
        self._developer_agent = developer_agent
        self._reviewer_agent = reviewer_agent
        self._output_agent = output_agent

    def select_next_speaker(self, messages: Sequence[AgentEvent | ChatMessage]):
        if len(messages) == 1:
            return self._developer_agent.name
        elif messages[-1].source == self._developer_agent.name:
            return self._reviewer_agent.name
        elif messages[-1].source is self._reviewer_agent.name:
            if self._is_code_approved(messages[-1].content):
                return self._output_agent.name
            else:
                return self._developer_agent.name
        else:
            return None

    async def start_chat(self, coding_request):
        termination_condition = TextMentionTermination("TERMINATE")
        self.groupchat = SelectorGroupChat(
            [
                self._developer_agent,
                self._reviewer_agent,
                self._output_agent,
            ],
            model_client=self._model_client,
            selector_func=self.select_next_speaker,
            max_turns=self._config.max_turns,
            termination_condition=termination_condition,
        )
        await Console(self.groupchat.run_stream(task=coding_request))

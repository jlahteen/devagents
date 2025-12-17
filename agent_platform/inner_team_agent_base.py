from typing import Sequence

from autogen_agentchat.agents import SocietyOfMindAgent
from autogen_agentchat.base import TerminationCondition
from autogen_agentchat.messages import AgentEvent, ChatMessage
from autogen_agentchat.teams import SelectorGroupChat
from autogen_core.models import ChatCompletionClient

from agent_platform.agent_base import AgentBase, Message, SpeakerSelectorFunc
from utils.config import Config


class InnerTeamAgentBase(SocietyOfMindAgent):
    """
    Defines a base class for agents with an inner team with a platform-agnostic interface.

    Internal implementation uses Autogen's SocietyOfMindAgent and SelectorGroupChat.
    """

    def __init__(
        self,
        name: str,
        config: Config,
        agents: list[AgentBase],
        speaker_selector: SpeakerSelectorFunc,
        termination_condition: TerminationCondition,
        system_message: str,
        response_prompt: str,
    ):
        """Initializes the inner team agent."""

        self._config = config
        self._agents = agents
        self._speaker_selector = speaker_selector
        self._termination_condition = termination_condition
        self._system_message = system_message
        self._response_prompt = response_prompt

        model_client = ChatCompletionClient.load_component(config.model_client)
        team = self._create_platform_team(model_client)

        super().__init__(
            name=name,
            team=team,
            model_client=model_client,
            instruction=self._system_message,
            response_prompt=self._response_prompt,
        )

    def _create_platform_team(self, model_client: ChatCompletionClient) -> SelectorGroupChat:
        """Creates the Autogen SelectorGroupChat from the AgentBase instances."""

        return SelectorGroupChat(
            self._agents,
            model_client=model_client,
            selector_func=self._select_next_speaker,
            termination_condition=self._termination_condition,
        )

    def _select_next_speaker(self, messages: Sequence[AgentEvent | ChatMessage]) -> str:
        """Selects the next speaker. Passes the last message to speaker_selector."""

        message_count = len(messages)
        last_message = None
        if message_count > 0:
            msg = messages[-1]
            last_message = Message(source=msg.source, content=getattr(msg, "content", ""))
        return self._speaker_selector(message_count, last_message)

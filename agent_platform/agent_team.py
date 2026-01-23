from typing import Sequence

from autogen_agentchat.base import TerminationCondition
from autogen_agentchat.messages import AgentEvent, ChatMessage
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console
from autogen_core.models import ChatCompletionClient

from agent_platform.agent_base import AgentBase, Message, SpeakerSelectorFunc
from utils.config import Config

# Define a const for the AutoGen MAX_TURNS setting
_MAX_TURNS = 999


class AgentTeam:
    """
    Defines a platform-agnostic agent team abstraction.

    Internal implementation is based on AutoGen's SelectorGroupChat.
    """

    def __init__(
        self,
        agents: list[AgentBase],
        config: Config,
        selector_func: SpeakerSelectorFunc,
        termination_condition: TerminationCondition,
    ):
        """Initialize an AgentTeam with a selector function for agent orchestration."""

        self._selector_func = selector_func
        model_client = ChatCompletionClient.load_component(config.model_client)
        self._team = SelectorGroupChat(
            participants=agents,
            model_client=model_client,
            selector_func=self._select_next_speaker,
            termination_condition=termination_condition,
            max_turns=_MAX_TURNS,
        )

    def _select_next_speaker(self, messages: Sequence[AgentEvent | ChatMessage]) -> str | None:
        """Selects the next speaker. Passes the last message to speaker_selector."""

        message_count = len(messages)
        last_message = None
        if message_count > 0:
            msg = messages[-1]
            last_message = Message(source=msg.source, content=getattr(msg, "content", ""))
        return self._selector_func(message_count, last_message)

    async def run(self, prompt: str) -> None:
        """Runs the team with the given prompt."""

        await Console(self._team.run_stream(task=prompt))

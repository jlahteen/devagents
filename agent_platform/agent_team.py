from agent_framework import GroupChatBuilder, GroupChatState

from agent_platform.agent_base import AgentBase, Message, SpeakerSelectorFunc
from agent_platform.console_printer import ConsolePrinter
from agent_platform.termination import MessageTermination
from utils.config import Config

# Define a const for the maximum conversation rounds
_MAX_CONVERSATION_ROUNDS = 1000


class AgentTeam:
    """
    Defines a platform-agnostic agent team abstraction.

    Internal implementation uses Microsoft Agent Framework's GroupChat.
    """

    def __init__(
        self,
        agents: list[AgentBase],
        config: Config,
        selector_func: SpeakerSelectorFunc,
        termination_condition: MessageTermination,
    ):
        """Initializes an AgentTeam with a MAF implementation."""

        self._agents = agents
        self._selector_func = selector_func
        self._termination_condition = termination_condition
        self._console_printer = ConsolePrinter()

        # Build a GroupChat with speaker selection
        self._workflow = (
            GroupChatBuilder()
            .participants(agents)
            .with_select_speaker_func(self._select_next_speaker)
            .with_termination_condition(self._termination_condition_wrapper)
            .with_max_rounds(_MAX_CONVERSATION_ROUNDS)
            .build()
        )

    async def run(self, prompt: str) -> None:
        """Runs the team with the given prompt."""

        # Print the user prompt first
        self._console_printer.print_user_prompt(prompt)

        # Stream workflow events in real-time
        async for event in self._workflow.run_stream(prompt, include_status_events=True):
            self._console_printer.print_event(event)

        self._console_printer.print_separator()

    def _select_next_speaker(self, state: GroupChatState) -> str:
        """Selects the next speaker in the conversation."""

        message_count = len(state.conversation)
        last_message = None

        # Get the agent names from the team
        valid_sources = {agent.name for agent in self._agents}

        if len(state.conversation) > 0:
            # Find the last message from a valid source
            # Skip internal messages like "group_chat_orchestrator"
            for msg in reversed(state.conversation):
                author = getattr(msg, "author_name", "")
                if author in valid_sources:
                    last_message = Message(source=author, content=msg.text)
                    break

        return self._selector_func(message_count, last_message)

    async def _termination_condition_wrapper(self, messages) -> bool:
        """Checks the termination condition."""

        return self._termination_condition.check(messages)

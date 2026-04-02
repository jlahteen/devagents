from agent_framework import ChatAgent, GroupChatBuilder, GroupChatState
from agent_framework._types import ChatMessage
from agent_framework.azure import AzureOpenAIChatClient

from agent_platform.agent_base import AgentBase, Message, SpeakerSelectorFunc
from agent_platform.console_printer import ConsolePrinter
from agent_platform.history_optimizer import HistoryOptimizer
from agent_platform.termination import SuccessOrFailureTermination
from utils.config import Config

# Define a constant for the maximum conversation rounds
_MAX_CONVERSATION_ROUNDS = 999


class InnerTeamAgentBase(ChatAgent):
    """
    Defines a platform-agnostic base class for agents with an inner team.

    Internal implementation inherits from ChatAgent and overrides run_stream() to execute the inner workflow. Returns
    a response based on a specified response prompt.
    """

    def __init__(
        self,
        name: str,
        config: Config,
        agents: list[AgentBase],
        speaker_selector: SpeakerSelectorFunc,
        termination_condition: SuccessOrFailureTermination,
        system_message: str,
        response_prompt: str,
        team_lead_agent_name: str,
        history_optimizer: HistoryOptimizer | None = None,
        forward_outer_prompt: bool = False,
    ):
        """Initializes a new inner team agent."""

        # Create a chat client using the config values
        model_config = config.model_client["config"]
        chat_client = AzureOpenAIChatClient(
            api_key=model_config.get("api_key"),
            endpoint=model_config.get("azure_endpoint"),
            deployment_name=model_config.get("azure_deployment"),
            api_version=model_config.get("api_version"),
        )

        # Initialize the base class
        super().__init__(
            chat_client=chat_client,
            instructions=system_message,
            name=name,
        )

        self._config = config
        self._agents = agents
        self._speaker_selector = speaker_selector
        self._termination_condition = termination_condition
        self._response_prompt = response_prompt
        self._console_printer = ConsolePrinter()
        self._team_lead_agent_name = team_lead_agent_name
        self._history_optimizer = history_optimizer
        self._forward_outer_prompt = forward_outer_prompt

        # Build the inner team workflow
        self._inner_workflow = (
            GroupChatBuilder()
            .participants(agents)
            .with_select_speaker_func(self._select_next_speaker)
            .with_termination_condition(self._termination_condition_wrapper)
            .with_max_rounds(_MAX_CONVERSATION_ROUNDS)
            .build()
        )

    async def run_stream(self, messages=None, *, thread=None, **kwargs):
        """
        Overrides run_stream() to execute an inner workflow and return its response to the outer GroupChat.

        In the end, we must call super().run_stream() to maintain conversation threading in the outer GroupChat. We
        also build a response prompt that instructs the LLM how to respond to the outer chat. The outer chat is not
        interested in the inner team's conversation history, just in the final result.
        """

        # Get the prompt for the inner team
        inner_prompt = self._get_inner_team_prompt(messages)

        events = []
        async for event in self._inner_workflow.run_stream(inner_prompt, include_status_events=True):
            self._console_printer.print_event(event)
            events.append(event)

        # Extract the final message from WorkflowOutputEvents
        final_message = ""
        for event in reversed(events):
            if event.__class__.__name__ == "WorkflowOutputEvent":
                if hasattr(event, "data") and event.data:
                    # Search backwards for the team_lead_agent message
                    for msg in reversed(event.data):
                        if (
                            hasattr(msg, "author_name")
                            and msg.author_name == self._team_lead_agent_name
                            and hasattr(msg, "text")
                            and msg.text
                            and msg.text.strip()
                        ):
                            final_message = msg.text
                            break
                    if final_message:
                        break

        if not final_message:
            final_message = "Inner team error: No result from the inner team"

        # Show that this agent is now working to return the response to the outer chat
        self._console_printer.print_working_agent(self.name)

        # Use the response prompt to relay the inner team's result to the outer chat
        response_prompt = f"{self._response_prompt}\n\n{final_message}"

        # Call the parent ChatAgent.run_stream() with the response prompt
        async for update in super().run_stream(
            messages=[ChatMessage(role="user", text=response_prompt)], thread=thread, **kwargs
        ):
            yield update

    async def run_inner_team(self, prompt: str):
        """Runs the inner team with a given prompt."""

        self._console_printer.print_user_prompt(prompt)
        async for event in self._inner_workflow.run_stream(prompt, include_status_events=True):
            self._console_printer.print_event(event)
        self._console_printer.print_separator()

    def _get_inner_team_prompt(self, messages) -> str:
        """Returns the prompt for the inner team."""

        if self._forward_outer_prompt:
            if isinstance(messages, list):
                for message in reversed(messages):
                    text = getattr(message, "text", None)
                    if text and text.strip():
                        return text.strip()

            text = getattr(messages, "text", None)
            if text and text.strip():
                return text.strip()

            if isinstance(messages, str) and messages.strip():
                return messages.strip()

        return "Begin."

    def _select_next_speaker(self, state: GroupChatState) -> str:
        """Selects the next speaker in the inner team workflow."""

        # Optimize the conversation history if a history optimizer is provided
        if self._history_optimizer is not None:
            self._history_optimizer.trim(state)

        message_count = len(state.conversation)
        last_message = None

        if len(state.conversation) > 0:
            msg = state.conversation[-1]
            # Use the author_name if available, otherwise an empty string
            author = msg.author_name if hasattr(msg, "author_name") and msg.author_name else ""
            last_message = Message(source=author, content=msg.text)

        next_speaker = self._speaker_selector(message_count, last_message)
        self._console_printer.print_working_agent(self.name, next_speaker)
        return next_speaker

    async def _termination_condition_wrapper(self, messages) -> bool:
        """Checks the termination condition."""

        return await self._termination_condition.check(messages)

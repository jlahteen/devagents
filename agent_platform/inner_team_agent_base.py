from agent_framework import Agent, AgentResponse, AgentResponseUpdate, Content, ResponseStream
from agent_framework.orchestrations import GroupChatBuilder, GroupChatState
from agent_framework.azure import AzureOpenAIChatClient

from agent_platform.agent_base import AgentBase, Message, SpeakerSelectorFunc
from agent_platform.console_printer import ConsolePrinter
from agent_platform.history_optimizer import HistoryOptimizer
from agent_platform.termination import SuccessOrFailureTermination
from utils.config import Config

# Define a constant for the maximum conversation rounds
_MAX_CONVERSATION_ROUNDS = 999


class InnerTeamAgentBase(Agent):
    """
    Defines a platform-agnostic base class for agents with an inner team.

    Internal implementation inherits from Agent and overrides run() to execute the inner workflow. Returns
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
            client=chat_client,
            instructions=system_message,
            name=name,
        )

        self._config = config
        self._agents = agents
        self._speaker_selector = speaker_selector
        self._termination_condition = termination_condition
        self._system_message = system_message
        self._response_prompt = response_prompt
        self._console_printer = ConsolePrinter()
        self._team_lead_agent_name = team_lead_agent_name
        self._history_optimizer = history_optimizer

        # Build the inner team workflow
        self._inner_workflow = (
            GroupChatBuilder(
                participants=agents,
                selection_func=self._select_next_speaker,
                termination_condition=self._termination_condition_wrapper,
                max_rounds=_MAX_CONVERSATION_ROUNDS,
            ).build()
        )

    def run(self, messages=None, *, stream=False, session=None, **kwargs):
        """
        Overrides run() to execute an inner workflow and return its response to the outer GroupChat.

        Returns a ResponseStream wrapping the inner team execution so the framework can iterate it with stream=True.
        """
        return ResponseStream.from_awaitable(self._run_inner_and_relay(session=session))

    async def _run_inner_and_relay(self, session=None) -> ResponseStream:
        """
        Runs the inner workflow, extracts the team lead result, then returns the parent's ResponseStream.

        This coroutine returns a ResponseStream (not an AgentResponse), satisfying ResponseStream.from_awaitable().
        """

        # Run the inner workflow with the system message (contains instructions for the inner team)
        inner_stream = self._inner_workflow.run(self._system_message, stream=True, include_status_events=True)
        async for event in inner_stream:
            self._console_printer.print_event(event)

        # Extract the final message from the workflow outputs
        result = await inner_stream.get_final_response()
        final_message = ""
        for output in result.get_outputs():
            if isinstance(output, list):
                for msg in reversed(output):
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

        # Return the final message directly as a ResponseStream — no extra LLM call needed
        text = final_message

        async def _text_gen():
            yield AgentResponseUpdate(
                contents=[Content.from_text(text)],
                role="assistant",
                author_name=self.name,
            )

        return ResponseStream(_text_gen(), finalizer=AgentResponse.from_updates)

    async def run_inner_team(self, prompt: str):
        """Runs the inner team with a given prompt."""

        self._console_printer.print_user_prompt(prompt)
        async for event in self._inner_workflow.run(prompt, stream=True, include_status_events=True):
            self._console_printer.print_event(event)
        self._console_printer.print_separator()

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
        return next_speaker

    async def _termination_condition_wrapper(self, messages) -> bool:
        """Checks the termination condition."""

        return await self._termination_condition.check(messages)

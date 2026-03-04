from typing import Any, Optional

# Define a const for the separator line width
_SEPARATOR_WIDTH = 60


class ConsolePrinter:
    """
    Defines a generic console printer for the workflow events.

    ConsolePrinter handles common event types raised by Microsoft Agent Framework.
    """

    def __init__(self):
        pass

    def print_event(self, event: Any):
        """Prints a workflow event to the console."""

        event_type = type(event).__name__
        workflow_event_type = getattr(event, "type", None)

        # Always print events that carry agent text, regardless of type
        if self._has_text_content(event):
            self._print_text_content(event)
            return

        # group_chat event: fires when a participant is selected — print their working header
        if workflow_event_type == "group_chat":
            data = getattr(event, "data", None)
            if type(data).__name__ == "GroupChatRequestSentEvent":
                participant_name = getattr(data, "participant_name", None)
                if participant_name:
                    self.print_working_agent(participant_name)
            return

        # Filter out noisy infrastructure events
        if self._should_filter_event(event_type, workflow_event_type):
            return

        # Delegate remaining events
        if "output" in event_type.lower() or "response" in event_type.lower() or workflow_event_type == "output":
            self._print_output(event)
        elif "fail" in event_type.lower() or "error" in event_type.lower() or workflow_event_type == "failed":
            self._print_error(event)
        else:
            self._print_unrecognized_event(event)

    def print_user_prompt(self, prompt: str):
        """Prints a user prompt."""

        print()
        try:
            print("👤 user says >>")
        except UnicodeEncodeError:
            print("[USER] user says >>")
        print("-" * _SEPARATOR_WIDTH)
        print(prompt)
        print()

    def print_working_agent(self, agent: str, sub_agent: Optional[str] = None):
        """Prints a line indicating the currently working agent."""

        display_name = f"{agent}.{sub_agent}" if sub_agent else agent
        print("\n")
        try:
            print(f"\033[92m🤖 {display_name} working...\033[0m")
        except UnicodeEncodeError:
            print(f"\033[92m[~~~] {display_name} working...\033[0m")
        print("-" * _SEPARATOR_WIDTH)

    def print_separator(self):
        """Prints a separator line."""

        print("\n" + "=" * _SEPARATOR_WIDTH + "\n")

    def _print_agent_response(self, content: str):
        """Prints an agent response."""

        try:
            print(content, flush=True)
        except UnicodeEncodeError:
            print(content.encode("ascii", errors="ignore").decode(), flush=True)

    def _should_filter_event(self, event_type: str, workflow_event_type: str | None = None) -> bool:
        """Checks whether an event should be filtered out."""

        # Filter by WorkflowEvent.type string (new rc2 API emits all events as WorkflowEvent)
        if workflow_event_type is not None:
            _FILTERED_WORKFLOW_EVENT_TYPES = {
                "executor_invoked",
                "executor_completed",
                "superstep_started",
                "superstep_completed",
                "started",
                "status",
            }
            if workflow_event_type in _FILTERED_WORKFLOW_EVENT_TYPES:
                return True

        # Filter by class name (legacy / in-process events)
        event_type_lower = event_type.lower()
        return (
            "workflowstarted" in event_type_lower
            or "workflowoutput" in event_type_lower
            or "workflowstatus" in event_type_lower
            or "groupchatrequestsent" in event_type_lower
            or "invoke" in event_type_lower
            or "started" in event_type_lower
            or "completed" in event_type_lower
        )

    def _has_text_content(self, event: Any) -> bool:
        """Checks whether an event has text content to display."""

        return self._extract_text(event) is not None

    def _extract_text(self, event: Any) -> str | None:
        """Extracts displayable text from an event, returning None if not present."""

        data = getattr(event, "data", None)
        if data is None:
            return None

        # Skip AgentExecutorResponse — its text was already printed token-by-token
        # via the streaming AgentResponseUpdate events above.
        if hasattr(data, "agent_response"):
            return None

        # Streaming AgentResponseUpdate: data.text
        if hasattr(data, "text") and data.text:
            return data.text

        return None

    def _print_text_content(self, event: Any):
        """Prints an event with a text content."""

        content = self._extract_text(event)
        if content:
            self._print_agent_response(content)

    def _print_error(self, event: Any):
        """Prints an error event."""

        error_msg = str(event)
        print(f"\n❌ Workflow error: {error_msg}\n")

    def _print_unrecognized_event(self, event: Any):
        """Prints an unrecognized event."""

        event_type = type(event).__name__
        print(f"\n[Event: {event_type}] {str(event)}\n")

    def _print_output(self, event: Any):
        """Prints an output/response event."""

        data = getattr(event, "data", None)
        # Only print if it's a string, skip raw objects
        if isinstance(data, str):
            self._print_agent_response(data)

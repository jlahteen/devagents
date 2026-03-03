from typing import Any

from agent_framework import GroupChatState


class HistoryOptimizer:
    """Defines a base class for conversation history optimizers."""

    def trim(self, messages: Any) -> None:
        """Optimizes conversation history. Expects messages to be a platform-dependent type."""
        pass


class MessageCountOptimizer(HistoryOptimizer):
    """A history optimizer that keeps only the most recent max_messages in the conversation history."""

    def __init__(self, max_messages: int):
        self._max_messages = max_messages

    def trim(self, messages: Any) -> None:
        """Trims conversation history to keep only the most recent max_messages in the conversation history."""

        if len(messages) > self._max_messages:
            del messages[: -self._max_messages]


class IterationOptimizer(HistoryOptimizer):
    """A history optimizer that keeps only the most recent max_iterations in the conversation history."""

    def __init__(self, team_lead_agent_name: str, max_iterations: int):
        self._team_lead_agent_name = team_lead_agent_name
        self._max_iterations = max_iterations

    def trim(self, messages: Any) -> None:
        """Trims the conversation history to keep only the most recent max_iterations in the conversation history."""

        state: GroupChatState = messages
        if not state or not hasattr(state, "messages") or not state.messages:
            return
        team_lead_name = self._team_lead_agent_name
        team_lead_count = 0
        cutoff_index = 0
        for i in range(len(state.messages) - 1, -1, -1):
            msg = state.messages[i]
            if msg.author_name == team_lead_name:
                team_lead_count += 1
                if team_lead_count >= self._max_iterations:
                    cutoff_index = i
                    break
        if cutoff_index > 0:
            del state.messages[:cutoff_index]

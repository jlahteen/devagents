from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Awaitable, Callable

from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import ChatCompletionClient
from autogen_core.tools import FunctionTool

from utils.config import Config

"""Define a platform-agnostic tool type."""
Tool = Callable[..., Any] | Callable[..., Awaitable[Any]]


@dataclass
class Message:
    """Defines a platform-agnostic message type."""

    source: str
    content: str


"""Define a platform-agnostic speaker selector function type."""
SpeakerSelectorFunc = Callable[[int, str | None, str | None], str]


class AgentBase(AssistantAgent):
    """Defines an AutoGen implementation for the platform-agnostic AgentBase."""

    def __init__(self, name: str, system_message: str, config: Config, tools: list[Tool] | None = None):
        self.config = config
        self._tools = tools or []

        super().__init__(
            name=name,
            system_message=system_message,
            model_client=ChatCompletionClient.load_component(config.model_client),
            tools=self._to_autogen_tools(),
        )

    def _to_autogen_tools(self):
        """Converts platform-agnostic tools to Autogen tools."""

        autogen_tools = []
        for tool in self._tools:
            # Wrap plain functions in FunctionTool with the name and description
            func_name = tool.__name__ if hasattr(tool, "__name__") else "tool"
            func_desc = tool.__doc__ or f"Tool: {func_name}"
            autogen_tools.append(FunctionTool(func=tool, description=func_desc))
        return autogen_tools

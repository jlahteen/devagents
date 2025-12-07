from typing import Any, Awaitable
from collections.abc import Callable

from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import ChatCompletionClient
from autogen_core.tools import FunctionTool

from utils.config import Config

# Framework-agnostic tool type
Tool = Callable[..., Any] | Callable[..., Awaitable[Any]]


class AgentBase(AssistantAgent):
    """A base class for agents inheriting from a platform agent."""

    def __init__(self, name: str, system_message: str, config: Config, tools: list[Tool] | None = None):
        self.config = config
        self._tools = tools or []
        
        super().__init__(
            name=name,
            system_message=system_message,
            model_client=ChatCompletionClient.load_component(config.model_client),
            tools=self._to_autogen_tools()
        )

    def _to_autogen_tools(self):
        """Converts framework-agnostic tools to Autogen tools."""

        autogen_tools = []
        for tool in self._tools:
            # Wrap plain functions in FunctionTool with name and description
            func_name = tool.__name__ if hasattr(tool, '__name__') else 'tool'
            func_desc = tool.__doc__ or f"Tool: {func_name}"
            autogen_tools.append(FunctionTool(func=tool, description=func_desc))
        return autogen_tools

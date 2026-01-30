from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Awaitable

from agent_framework import ChatAgent, ai_function
from agent_framework.azure import AzureOpenAIChatClient

from utils.config import Config

"""Define a platform-agnostic tool type."""
Tool = Callable[..., Any] | Callable[..., Awaitable[Any]]


@dataclass
class Message:
    """Defines a platform-agnostic message type."""

    source: str
    content: str


"""Define a platform-agnostic speaker selector function type."""
SpeakerSelectorFunc = Callable[[int, Message | None], str]


class AgentBase(ChatAgent):
    """Defines a Microsoft Agent Framework implementation for the platform-agnostic AgentBase."""

    def __init__(self, name: str, system_message: str, config: Config, tools: list[Tool] | None = None):
        self._config = config
        self._tools = tools or []

        # Create a MAF chat client using the config values
        model_config = config.model_client["config"]
        chat_client = AzureOpenAIChatClient(
            api_key=model_config.get("api_key"),
            endpoint=model_config.get("azure_endpoint"),
            deployment_name=model_config.get("azure_deployment"),
            api_version=model_config.get("api_version"),
        )

        # Initialize the ChatAgent parent
        super().__init__(
            name=name,
            instructions=system_message,
            chat_client=chat_client,
            tools=self._to_maf_tools(),
        )

    async def run(self, prompt: str) -> str:
        """Runs the agent with a prompt. Returns the agent's response content."""

        response = await super().run(prompt)
        return response.messages[0].text if response.messages else ""

    def _to_maf_tools(self):
        """Converts the platform-agnostic tools to the corresponding MAF tools."""

        maf_tools = []
        for tool in self._tools:
            # Wrap plain functions using MAF's ai_function
            func_name = tool.__name__ if hasattr(tool, "__name__") else "tool"
            func_desc = tool.__doc__ or f"Tool: {func_name}"
            maf_tool = ai_function(func=tool, name=func_name, description=func_desc)
            maf_tools.append(maf_tool)
        return maf_tools

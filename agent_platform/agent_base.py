from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Awaitable

from agent_framework import ChatAgent, ai_function
from agent_framework.azure import AzureOpenAIChatClient
from agent_framework.exceptions import ServiceResponseException
from tenacity import AsyncRetrying, retry_if_exception, stop_after_attempt, wait_exponential

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

# Define constants for the retry logic
_MAX_RETRY_ATTEMPTS = 5
_RETRY_MIN_WAIT_SECONDS = 4
_RETRY_MAX_WAIT_SECONDS = 120
_RETRY_WAIT_MULTIPLIER = 1
_HTTP_STATUS_RATE_LIMIT = 429


def _is_rate_limit_error(exception: BaseException) -> bool:
    """Checks if the exception is a rate limit error."""

    if isinstance(exception, ServiceResponseException):
        # Check the inner exception for the HTTP status code
        inner = getattr(exception, "inner_exception", None)
        if inner and hasattr(inner, "status_code"):
            return inner.status_code == _HTTP_STATUS_RATE_LIMIT
        # Fallback to the string check
        error_msg = str(exception)
        return str(_HTTP_STATUS_RATE_LIMIT) in error_msg or "RateLimitReached" in error_msg
    return False


class RetryableAzureOpenAIChatClient(AzureOpenAIChatClient):
    """Wraps AzureOpenAIChatClient with the retry logic for rate limit errors."""

    async def _inner_get_streaming_response(self, **kwargs):
        """Overrides the base class method to add the retry logic for rate limit errors."""

        attempt = 0
        async for attempt_context in AsyncRetrying(
            retry=retry_if_exception(_is_rate_limit_error),
            stop=stop_after_attempt(_MAX_RETRY_ATTEMPTS),
            wait=wait_exponential(
                multiplier=_RETRY_WAIT_MULTIPLIER, min=_RETRY_MIN_WAIT_SECONDS, max=_RETRY_MAX_WAIT_SECONDS
            ),
            reraise=True,
        ):
            with attempt_context:
                attempt += 1
                try:
                    async for result in super()._inner_get_streaming_response(**kwargs):
                        yield result
                    return
                except Exception as ex:
                    if _is_rate_limit_error(ex):
                        wait_time = min(_RETRY_MAX_WAIT_SECONDS, int(2**attempt * 2))
                        print(
                            f"⚠️  Rate limit (429) hit - retrying in {wait_time}s (attempt {attempt}/{_MAX_RETRY_ATTEMPTS})..."
                        )
                    raise


class AgentBase(ChatAgent):
    """Defines a Microsoft Agent Framework implementation for the platform-agnostic AgentBase."""

    def __init__(self, name: str, system_message: str, config: Config, tools: list[Tool] | None = None):
        self._config = config
        self._tools = tools or []

        # Create a MAF chat client using the config values
        model_config = config.model_client["config"]
        chat_client = RetryableAzureOpenAIChatClient(
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

        # Extract the final text response
        if not response.messages:
            return ""

        # Return the last non-empty text message
        for msg in reversed(response.messages):
            if hasattr(msg, "text") and msg.text:
                return msg.text

        return ""

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

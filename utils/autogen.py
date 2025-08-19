import asyncio
from typing import Callable, Optional, Sequence

from autogen_agentchat.base import TerminationCondition
from autogen_agentchat.messages import BaseAgentEvent, BaseChatMessage, StopMessage


class SuccessOrFailureTermination(TerminationCondition):
    def __init__(
        self, success_phrase: str, failure_phrase: str, on_failure_callback: Optional[Callable[[str], None]] = None
    ) -> None:
        self._success_phrase = success_phrase
        self._failure_phrase = failure_phrase
        self._on_failure_callback = on_failure_callback
        self._terminated = False

    @property
    def terminated(self) -> bool:
        return self._terminated

    async def __call__(self, messages: Sequence[BaseAgentEvent | BaseChatMessage]) -> StopMessage | None:
        if self._terminated:
            return None

        # Search from the last message backwards
        for message in reversed(messages):
            if hasattr(message, "content") and isinstance(message.content, str):
                if self._success_phrase in message.content:
                    self._terminated = True
                    return StopMessage(
                        content=f"Success phrase '{self._success_phrase}' found in a message",
                        source="SuccessOrFailureTermination",
                    )
                if self._failure_phrase in message.content:
                    self._terminated = True
                    # Call the failure callback if provided
                    if self._on_failure_callback is not None:
                        if asyncio.iscoroutinefunction(self._on_failure_callback):
                            await self._on_failure_callback(message.content)
                        else:
                            self._on_failure_callback(message.content)
                    return StopMessage(
                        content=f"Failure phrase '{self._failure_phrase}' found in a message",
                        source="SuccessOrFailureTermination",
                    )
        return None

    async def reset(self) -> None:
        self._terminated = False

    def dump_component(self):
        # Callbacks are not serialized; store as None
        return {
            "type": "SuccessOrFailureTermination",
            "success_phrase": self._success_phrase,
            "failure_phrase": self._failure_phrase,
            "on_failure_callback": None,
        }

    @classmethod
    def load_component(cls, config):
        # Callback is not restored from config; initialize as None
        return cls(config["success_phrase"], config["failure_phrase"])

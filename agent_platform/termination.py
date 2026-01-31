import asyncio
from typing import Callable, Optional


class MessageTermination:
    """
    Defines a platform-agnostic termination condition that stops when a specific text is mentioned in the conversation.
    """

    def __init__(self, text: str):
        self._text = text

    def check(self, conversation: list) -> bool:
        """Checks if the termination text appears in the conversation."""

        for message in reversed(conversation):
            if hasattr(message, "text") and self._text in message.text:
                return True
        return False


class SuccessOrFailureTermination:
    """
    Defines a platform-agnostic termination condition that terminates a conversation based on a success and failure
    phrase.
    """

    def __init__(
        self, success_phrase: str, failure_phrase: str, on_failure_callback: Optional[Callable[[str], None]] = None
    ) -> None:
        """Initializes a SuccessOrFailureTermination instance."""

        self._success_phrase = success_phrase
        self._failure_phrase = failure_phrase
        self._on_failure_callback = on_failure_callback

    async def check(self, conversation: list) -> bool:
        """Checks if the success or failure phrase appears in the conversation."""

        # Search from the last message backwards
        for message in reversed(conversation):
            if hasattr(message, "text") and isinstance(message.text, str):
                if self._success_phrase in message.text:
                    return True
                if self._failure_phrase in message.text:
                    # Call the failure callback if provided
                    if self._on_failure_callback is not None:
                        if asyncio.iscoroutinefunction(self._on_failure_callback):
                            await self._on_failure_callback(message.text)
                        else:
                            self._on_failure_callback(message.text)
                    return True
        return False

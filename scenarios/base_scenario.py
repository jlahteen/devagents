from abc import ABC, abstractmethod
from autogen import ChatResult


class BaseScenario(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def run_scenario(self, prompt: str) -> ChatResult:
        pass

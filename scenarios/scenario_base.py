from abc import ABC, abstractmethod
from autogen import ChatResult
from config import Config


class ScenarioBase(ABC):
    """Defines an abstract base class for scenarios."""

    def __init__(self):
        pass

    @abstractmethod
    def run_scenario(self, prompt: str) -> ChatResult:
        pass


def create_scenario(scenario_name) -> ScenarioBase:
    """Creates a scenario based on a specified scenario name."""

    scenario = None
    match scenario_name:
        case "NewApp":
            from scenarios.new_app.new_app_scenario import NewAppScenario

            scenario = NewAppScenario(Config())
        case "NewCode":
            from scenarios.new_code.new_code_scenario import NewCodeScenario

            scenario = NewCodeScenario(Config())
        case _:
            print(f"Unknown scenario: '{scenario_name}'")
            exit(1)
    return scenario

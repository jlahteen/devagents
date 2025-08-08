from abc import ABC, abstractmethod

from config import Config
from scenarios.orchestrator_agent_base import OrchestratorAgentBase, OrchestratorAgentContext


class ScenarioBase(ABC):
    """Defines an abstract base class for scenarios."""

    def __init__(self):
        pass

    @abstractmethod
    async def create_orchestrator_agent(
        self, config: Config, context: OrchestratorAgentContext = None
    ) -> OrchestratorAgentBase:
        """Creates an orchestrator agent for the scenario."""
        pass

    @staticmethod
    def create_scenario(scenario_name) -> "ScenarioBase":
        """Creates a scenario based on a specified scenario name."""

        scenario = None
        match scenario_name:
            case "NewApp" | "new-app":
                from scenarios.new_app.new_app_scenario import NewAppScenario

                scenario = NewAppScenario()
            case "NewCode" | "new-code":
                from scenarios.new_code.new_code_scenario import NewCodeScenario

                scenario = NewCodeScenario()
            case "FixBuild" | "fix-build":
                from scenarios.fix_build.fix_build_scenario import FixBuildScenario

                scenario = FixBuildScenario()
            case "FixTests" | "fix-tests":
                from scenarios.fix_tests.fix_tests_scenario import FixTestsScenario

                scenario = FixTestsScenario()
            case _:
                raise ValueError(f"Unknown scenario: '{scenario_name}'")
        return scenario

from abc import ABC, abstractmethod

from workflows.orchestrator_base import OrchestratorBase, OrchestratorContext
from utils.config import Config


class ScenarioBase(ABC):
    """Defines an abstract base class for scenarios."""

    def __init__(self):
        pass

    @abstractmethod
    async def create_orchestrator(
        self, config: Config, context: OrchestratorContext = None
    ) -> OrchestratorBase:
        """Creates an orchestrator for the scenario."""
        pass

    @staticmethod
    def create_scenario(scenario_name) -> "ScenarioBase":
        """Creates a scenario based on a specified scenario name."""

        scenario = None
        match scenario_name:
            case "NewApp" | "new-app":
                from workflows.new_app.new_app_scenario import NewAppScenario

                scenario = NewAppScenario()
            case "ModifyApp" | "modify-app":
                from workflows.modify_app.modify_app_scenario import ModifyAppScenario

                scenario = ModifyAppScenario()
            case "NewCode" | "new-code":
                from workflows.new_code.new_code_scenario import NewCodeScenario

                scenario = NewCodeScenario()
            case "ModifyCode" | "modify-code":
                from workflows.modify_code.modify_code_scenario import ModifyCodeScenario

                scenario = ModifyCodeScenario()
            case "FixBuild" | "fix-build":
                from workflows.fix_build.fix_build_scenario import FixBuildScenario

                scenario = FixBuildScenario()
            case "FixTests" | "fix-tests":
                from workflows.fix_tests.fix_tests_scenario import FixTestsScenario

                scenario = FixTestsScenario()
            case _:
                raise ValueError(f"Unknown scenario: '{scenario_name}'")
        return scenario

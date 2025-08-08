from config import Config
from scenarios.fix_tests.fix_tests_orchestrator_agent import FixTestsOrchestratorAgent
from scenarios.orchestrator_agent_base import OrchestratorAgentBase, OrchestratorContext
from scenarios.scenario_base import ScenarioBase


class FixTestsScenario(ScenarioBase):
    """A scenario to ensure all tests pass successfully."""

    def create_orchestrator_agent(self, config: Config, context: OrchestratorContext = None) -> OrchestratorAgentBase:
        orchestrator_agent = FixTestsOrchestratorAgent(config=config, context=context)
        return orchestrator_agent

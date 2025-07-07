from agents.test_agent import TestAgent
from config import Config
from scenarios.fix_tests.fix_tests_orchestrator_agent import FixTestsOrchestratorAgent
from scenarios.orchestrator_agent_base import OrchestratorAgentBase
from scenarios.scenario_base import ScenarioBase


class FixTestsScenario(ScenarioBase):
    """A scenario to ensure all tests pass successfully."""

    def create_orchestrator_agent(self, config: Config) -> OrchestratorAgentBase:
        # Create the necessary agents

        # Test Agent
        test_agent = TestAgent(config=config)

        # Create an Orchestrator Agent
        orchestrator_agent = FixTestsOrchestratorAgent(config, test_agent)
        return orchestrator_agent

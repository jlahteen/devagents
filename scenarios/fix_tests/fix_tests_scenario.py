from agents.test_agent import TestAgent
from config import Config
from scenarios.fix_tests.fix_tests_orchestrator_agent import FixTestsOrchestratorAgent
from scenarios.scenario_base import ScenarioBase


class FixTestsScenario(ScenarioBase):
    """A scenario to ensure all tests pass successfully."""

    def __init__(self, config: Config):
        # Create the necessary agents

        # Test Agent
        test_agent = TestAgent(config=config)

        # Create an Orchestrator Agent
        self._orchestrator_agent = FixTestsOrchestratorAgent(config, test_agent)

    async def run_scenario(self, prompt: str) -> None:
        """Runs the scenario."""

        await self._orchestrator_agent.run_team(prompt)

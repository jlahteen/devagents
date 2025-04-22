from agents.build_agent import BuildAgent
from config import Config
from scenarios.fix_build_errors.fix_build_errors_orchestrator_agent import FixBuildErrorsOrchestratorAgent
from scenarios.scenario_base import ScenarioBase


class FixBuildErrorsScenario(ScenarioBase):
    """A scenario for fixing build errors."""

    def __init__(self, config: Config):
        # Create the necessary agents

        # Build Agent
        build_agent = BuildAgent(config=config)

        # Create an Orchestrator Agent
        self._orchestrator_agent = FixBuildErrorsOrchestratorAgent(config, build_agent)

    async def run_scenario(self, prompt: str) -> None:
        """Runs the scenario."""

        await self._orchestrator_agent.start_chat(prompt)

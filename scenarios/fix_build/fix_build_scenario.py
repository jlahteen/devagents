from agents.build_agent import BuildAgent
from config import Config
from scenarios.fix_build.fix_build_orchestrator_agent import FixBuildOrchestratorAgent
from scenarios.scenario_base import ScenarioBase


class FixBuildScenario(ScenarioBase):
    """A scenario to ensure an application builds successfully."""

    def __init__(self, config: Config):
        # Create the necessary agents

        # Build Agent
        build_agent = BuildAgent(config=config)

        # Create an Orchestrator Agent
        self._orchestrator_agent = FixBuildOrchestratorAgent(config, build_agent)

    async def run_scenario(self, prompt: str) -> None:
        """Runs the scenario."""

        await self._orchestrator_agent.run_team(prompt)

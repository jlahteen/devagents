from agents.build_agent import BuildAgent
from config import Config
from scenarios.fix_build.fix_build_orchestrator_agent import FixBuildOrchestratorAgent
from scenarios.orchestrator_agent_base import OrchestratorAgentBase
from scenarios.scenario_base import ScenarioBase


class FixBuildScenario(ScenarioBase):
    """A scenario to ensure an application builds successfully."""

    def create_orchestrator_agent(self, config: Config) -> OrchestratorAgentBase:
        # Create the necessary agents

        # Build Agent
        build_agent = BuildAgent(config=config)

        # Create an Orchestrator Agent
        orchestrator_agent = FixBuildOrchestratorAgent(config, build_agent)
        return orchestrator_agent

from config import Config
from scenarios.fix_build.fix_build_orchestrator_agent import FixBuildOrchestratorAgent
from scenarios.orchestrator_agent_base import OrchestratorAgentBase, OrchestratorContext
from scenarios.scenario_base import ScenarioBase


class FixBuildScenario(ScenarioBase):
    """A scenario to ensure an application builds successfully."""

    def create_orchestrator_agent(self, config: Config, context: OrchestratorContext = None) -> OrchestratorAgentBase:
        orchestrator_agent = FixBuildOrchestratorAgent(config=config, context=context)
        return orchestrator_agent

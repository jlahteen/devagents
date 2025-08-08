from config import Config
from scenarios.new_app.new_app_orchestrator_agent import NewAppOrchestratorAgent
from scenarios.orchestrator_agent_base import OrchestratorAgentBase, OrchestratorAgentContext
from scenarios.scenario_base import ScenarioBase


class NewAppScenario(ScenarioBase):
    """A scenario for creating a new application."""

    def create_orchestrator_agent(
        self, config: Config, context: OrchestratorAgentContext = None
    ) -> OrchestratorAgentBase:
        # Create an Orchestrator Agent
        orchestrator_agent = NewAppOrchestratorAgent(config=config, context=context)
        return orchestrator_agent

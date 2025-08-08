from config import Config
from scenarios.new_code.new_code_orchestrator_agent import NewCodeOrchestratorAgent
from scenarios.orchestrator_agent_base import OrchestratorAgentBase, OrchestratorAgentContext
from scenarios.scenario_base import ScenarioBase


class NewCodeScenario(ScenarioBase):
    """A scenario for creating new code snippets."""

    def create_orchestrator_agent(
        self, config: Config, context: OrchestratorAgentContext = None
    ) -> OrchestratorAgentBase:
        # Create an Orchestrator Agent
        orchestrator_agent = NewCodeOrchestratorAgent(config=config, context=context)
        return orchestrator_agent

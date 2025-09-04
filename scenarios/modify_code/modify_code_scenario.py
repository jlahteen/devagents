from scenarios.modify_code.modify_code_orchestrator_agent import ModifyCodeOrchestratorAgent
from scenarios.orchestrator_agent_base import OrchestratorAgentBase, OrchestratorContext
from scenarios.scenario_base import ScenarioBase
from utils.config import Config


class ModifyCodeScenario(ScenarioBase):
    """A scenario for modifying existing code files."""

    def create_orchestrator_agent(self, config: Config, context: OrchestratorContext = None) -> OrchestratorAgentBase:
        # Create an Orchestrator Agent
        orchestrator_agent = ModifyCodeOrchestratorAgent(config=config, context=context)
        return orchestrator_agent

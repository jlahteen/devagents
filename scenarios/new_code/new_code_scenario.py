from agents.developer_agent import DeveloperAgent
from agents.output_agent import OutputAgent
from agents.reviewer_agent import ReviewerAgent
from config import Config
from scenarios.new_code.new_code_orchestrator_agent import NewCodeOrchestratorAgent
from scenarios.orchestrator_agent_base import OrchestratorAgentBase
from scenarios.scenario_base import ScenarioBase


class NewCodeScenario(ScenarioBase):
    """A scenario for creating new code snippets."""

    def create_orchestrator_agent(self, config: Config) -> OrchestratorAgentBase:
        # Create the necessary agents

        # Developer Agent
        developer_agent = DeveloperAgent(config=config)

        # Reviewer Agent
        reviewer_agent = ReviewerAgent(config=config)

        # Output Agent
        output_agent = OutputAgent(config=config)

        # Create an Orchestrator Agent
        orchestrator_agent = NewCodeOrchestratorAgent(config, developer_agent, reviewer_agent, output_agent)
        return orchestrator_agent

from agents.build_agent import BuildAgent
from agents.developer_agent import DeveloperAgent
from agents.output_agent import OutputAgent
from agents.reviewer_agent import ReviewerAgent
from agents.scaffold_agent import ScaffoldAgent
from agents.test_agent import TestAgent
from config import Config
from scenarios.new_app.new_app_orchestrator_agent import NewAppOrchestratorAgent
from scenarios.orchestrator_agent_base import OrchestratorAgentBase
from scenarios.scenario_base import ScenarioBase


class NewAppScenario(ScenarioBase):
    """A scenario for creating a new application."""

    def create_orchestrator_agent(self, config: Config) -> OrchestratorAgentBase:
        # Create the necessary agents

        # Scaffold Agent
        scaffold_agent = ScaffoldAgent(config=config)

        # Developer Agent
        developer_agent = DeveloperAgent(config=config)

        # Reviewer Agent
        reviewer_agent = ReviewerAgent(config=config)

        # Output Agent
        output_agent = OutputAgent(config=config)

        # Build Agent
        build_agent = BuildAgent(config=config)

        # Test Agent
        test_agent = TestAgent(config=config)

        # Create an Orchestrator Agent
        orchestrator_agent = NewAppOrchestratorAgent(
            config, scaffold_agent, developer_agent, reviewer_agent, output_agent, build_agent, test_agent
        )
        return orchestrator_agent

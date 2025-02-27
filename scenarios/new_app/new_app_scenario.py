from agents.developer_agent import DeveloperAgent
from agents.output_agent import OutputAgent
from agents.reviewer_agent import ReviewerAgent
from agents.scaffold_agent import ScaffoldAgent
from config import Config
from scenarios.scenario_base import ScenarioBase
from scenarios.new_app.new_app_orchestrator_agent import NewAppOrchestratorAgent
from autogen import ChatResult


class NewAppScenario(ScenarioBase):
    """A scenario for creating a new application."""

    def __init__(self, config: Config):
        # Create the necessary agents

        # Scaffold Agent
        scaffold_agent = ScaffoldAgent(config=config)

        # Developer Agent
        developer_agent = DeveloperAgent(config=config)

        # Reviewer Agent
        reviewer_agent = ReviewerAgent(config=config)

        # Output Agent
        output_agent = OutputAgent(config=config)

        # Create an Orchestrator Agent
        self._orchestrator_agent = NewAppOrchestratorAgent(
            config, scaffold_agent, developer_agent, reviewer_agent, output_agent
        )

    def run_scenario(self, prompt: str) -> ChatResult:
        """Runs the scenario."""

        chat_result = self._orchestrator_agent.start_chat(prompt)
        return chat_result

from agents.developer_agent import DeveloperAgent
from agents.output_agent import OutputAgent
from agents.reviewer_agent import ReviewerAgent
from agents.scaffold_agent import ScaffoldAgent
from config import Config
from scenarios.base_scenario import BaseScenario
from scenarios.new_app.orchestrator_agent import OrchestratorAgent
from autogen import ChatResult


class NewAppScenario(BaseScenario):
    """A scenario for creating a new appliaction."""

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
        self._orchestrator_agent = OrchestratorAgent(
            config, scaffold_agent, developer_agent, reviewer_agent, output_agent
        )

    def run_scenario(self, prompt: str) -> ChatResult:
        """Runs the scenario."""

        chat_result = self._orchestrator_agent.start_chat(prompt)
        return chat_result

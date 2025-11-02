from scenarios.app_scenario_orchestrator_agent_base import AppScenarioOrchestratorAgentBase
from scenarios.orchestrator_agent_base import OrchestratorContext
from utils.config import Config
from utils.constants import ScenarioType


class NewAppOrchestratorAgent(AppScenarioOrchestratorAgentBase):
    """An orchestrator agent to run a NewApp scenario."""

    def __init__(
        self,
        config: Config,
        context: OrchestratorContext = None,
    ):
        super().__init__(
            config=config,
            scenario_type=ScenarioType.NEW_APP,
            context=context,
        )

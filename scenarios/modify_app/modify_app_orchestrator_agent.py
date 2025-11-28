from scenarios.app_scenario_orchestrator_agent_base import AppScenarioOrchestratorAgentBase
from scenarios.orchestrator_agent_base import OrchestratorContext
from utils.config import Config
from utils.constants import ScenarioType


class ModifyAppOrchestratorAgent(AppScenarioOrchestratorAgentBase):
    """An orchestrator agent to run a ModifyApp scenario."""

    def __init__(
        self,
        config: Config,
        context: OrchestratorContext = None,
    ):
        super().__init__(
            config=config,
            scenario_type=ScenarioType.MODIFY_APP,
            context=context,
        )

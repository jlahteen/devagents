from scenarios.code_scenario_orchestrator_agent_base import CodeScenarioOrchestratorAgentBase
from scenarios.orchestrator_agent_base import OrchestratorContext
from utils.config import Config
from utils.constants import ScenarioType


class NewCodeOrchestratorAgent(CodeScenarioOrchestratorAgentBase):
    """An orchestrator agent to run a NewCode scenario."""

    def __init__(
        self,
        config: Config,
        context: OrchestratorContext = None,
    ):
        super().__init__(
            config=config,
            scenario_type=ScenarioType.NEW_CODE,
            context=context,
        )

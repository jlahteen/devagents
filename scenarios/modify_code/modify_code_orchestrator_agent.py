from scenarios.code_scenario_orchestrator_agent_base import CodeScenarioOrchestratorAgentBase
from scenarios.orchestrator_agent_base import OrchestratorContext
from utils.config import Config
from utils.constants import ScenarioType


class ModifyCodeOrchestratorAgent(CodeScenarioOrchestratorAgentBase):
    """An orchestrator agent to run a ModifyCode scenario."""

    def __init__(
        self,
        config: Config,
        context: OrchestratorContext = None,
    ):
        super().__init__(
            config=config,
            scenario_type=ScenarioType.MODIFY_CODE,
            context=context,
        )

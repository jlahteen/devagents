from scenarios.code_scenario_orchestrator_base import CodeScenarioOrchestratorBase
from scenarios.orchestrator_base import OrchestratorContext
from utils.config import Config
from utils.constants import ScenarioType


class ModifyCodeOrchestrator(CodeScenarioOrchestratorBase):
    """An orchestrator to run a ModifyCode scenario."""

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

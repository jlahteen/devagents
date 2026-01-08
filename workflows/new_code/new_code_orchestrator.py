from workflows.code_scenario_orchestrator_base import CodeScenarioOrchestratorBase
from workflows.orchestrator_base import OrchestratorContext
from utils.config import Config
from utils.constants import ScenarioType


class NewCodeOrchestratorAgent(CodeScenarioOrchestratorBase):
    """An orchestrator to run a NewCode scenario."""

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

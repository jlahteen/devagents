import textwrap

from agent_platform.agent_base import AgentBase
from utils.config import Config
from utils.constants import JUDGE_AGENT_APPROVED, JUDGE_AGENT_CHANGES_REQUIRED


class JudgeAgent(AgentBase):
    """An agent that validates whether the reviewer's feedback is within the developer's scope."""

    _system_message = textwrap.dedent(
        f"""
        ## ROLE
        You are an agent that works as a judge between the reviewer and the developer.

        ## TASK
        Your task is to validate whether the reviewer's feedback is within the developer's scope to implement.

        ## INSTRUCTIONS
        - Developer is only responsible for the code that the developer has written in the conversation using the
          @save_file or @delete_file markers.
        - Developer is NOT responsible for any actions taken in the scaffolding phase.
        - Response as follows:
          - Respond with '{JUDGE_AGENT_CHANGES_REQUIRED}' if ANY reviewer feedback is in-scope for the developer to
            implement.
            - In this case, do not include any other content in your response.
          - Respond with '{JUDGE_AGENT_APPROVED}' if ALL reviewer feedback is out-of-scope for the developer to
            implement.
            - In this case, include the reasoning behind your decision why the feedback is out-of-scope.
        """
    )

    def __init__(self, config: Config):
        super().__init__(
            name="judge_agent",
            system_message=self._system_message,
            config=config,
        )

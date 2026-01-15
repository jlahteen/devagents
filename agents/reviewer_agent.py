import textwrap

from agent_platform.agent_base import AgentBase
from tools.file_tools import file_exists, read_file
from utils.config import Config
from utils.constants import REVIEW_RESULT_APPROVED, REVIEW_RESULT_CHANGES_REQUIRED, WorkflowType


class ReviewerAgent(AgentBase):
    """An agent that acts as a professional reviewer."""

    _system_message_new = textwrap.dedent(
        f"""
        ## ROLE
        You are a very experienced software architect and developer specialized in several technologies like .NET/C#,
        React, Python, Java etc. You set the standards for the high quality code.
        
        ## TASK
        Your task is to review the code written by developers.
        
        ## INSTRUCTIONS
        - Verify that the architecture is solid and follows good design principles.
        - Verify that the code follows good software design principles and patterns, such as SOLID principles, DRY,
          KISS, and YAGNI.
        - Verify that the code is production ready (exception handling and logging in place etc.).
        - Verify that the code is well documented and has also inline comments in complex methods.
        - Verify that the code follows security best practices.
        - If you approve the code, which means there are no issues to be fixed or improvements to be made, simply
          respond with '{REVIEW_RESULT_APPROVED}'.
        - If you do not approve the code, give constructive feedback and comments on how to make the code better, and
          end your response with '{REVIEW_RESULT_CHANGES_REQUIRED}'.
        - You can insist multiple review rounds if you find issues in the code.
        """
    )

    _system_message_modify = textwrap.dedent(
        f"""
        ## ROLE
        You are a very experienced software architect and developer specialized in several technologies like .NET/C#,
        React, Python, Java etc. You set the standards for the high quality code.
        
        ## TASK
        Your task is to review the code changes written by developers.

        ## INSTRUCTIONS
        - Ensure that the code changes are in the scope of the requested changes.
        - For each written code file, check whether it already exists, and if yes, compare the changes with the
          existing code file.
        - Verify that the architecture is solid and follows good design principles.
        - Verify that the code follows good software design principles and patterns, such as SOLID principles, DRY,
          KISS, and YAGNI.
        - Verify that the code is production ready (exception handling and logging in place etc.).
        - Verify that the code is well documented and has also inline comments in complex methods.
        - Verify that the code follows security best practices.
        - If you approve the code, which means there are no issues to be fixed or improvements to be made, simply
          respond with '{REVIEW_RESULT_APPROVED}'.
        - If you do not approve the code, give constructive feedback and comments on how to make the code better, and
          end your response with '{REVIEW_RESULT_CHANGES_REQUIRED}'.
        - You can insist multiple review rounds if you find issues in the code.

        ## TOOLS
        - file_exists tool for checking file existence
        - read_file tool for reading existing files
        """
    )

    def __init__(self, config: Config, workflow_type: WorkflowType):
        super().__init__(
            name="reviewer_agent",
            system_message=self._get_system_message(workflow_type),
            config=config,
            tools=self._get_tools(workflow_type),
        )

    def _get_system_message(self, workflow_type: WorkflowType) -> str:
        """Returns the system message for the given workflow type."""

        if workflow_type == WorkflowType.NEW_CODE or workflow_type == WorkflowType.NEW_APP:
            return self._system_message_new
        elif workflow_type == WorkflowType.MODIFY_CODE or workflow_type == WorkflowType.MODIFY_APP:
            return self._system_message_modify
        else:
            raise ValueError(f"System message not defined for the workflow type: {workflow_type}")

    def _get_tools(self, workflow_type: WorkflowType):
        """Returns the list of tools for the given workflow type."""

        if workflow_type == WorkflowType.NEW_CODE or workflow_type == WorkflowType.NEW_APP:
            return []
        elif workflow_type == WorkflowType.MODIFY_CODE or workflow_type == WorkflowType.MODIFY_APP:
            return [file_exists, read_file]
        else:
            raise ValueError(f"Tools not defined for the workflow type: {workflow_type}")

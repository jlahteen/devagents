import textwrap

from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import ChatCompletionClient

from tools.file_tools import file_exists, read_file
from utils.config import Config
from utils.constants import REVIEW_RESULT_APPROVED, REVIEW_RESULT_CHANGES_REQUIRED, ScenarioType


class ReviewerAgent(AssistantAgent):
    """An agent that acts as a professional reviewer."""

    _system_message_new = textwrap.dedent(
        f"""
        ## Role
        You are a very experienced software architect and developer specialized in several technologies like .NET/C#,
        React, Python, Java etc. You set the standards for the high quality code.
        
        ## Task
        Your task is to review the code written by developers.
        
        ## Instructions
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
        ## Role
        You are a very experienced software architect and developer specialized in several technologies like .NET/C#,
        React, Python, Java etc. You set the standards for the high quality code.
        
        ## Task
        Your task is to review the code changes written by developers.

        ## Instructions
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

        ## Tools
        - file_exists tool for checking file existence
        - read_file tool for reading existing files
        """
    )

    def __init__(self, config: Config, scenario_type: ScenarioType):
        super().__init__(
            name="reviewer_agent",
            system_message=self._get_system_message(scenario_type),
            tools=self._get_tools(scenario_type),
            model_client=ChatCompletionClient.load_component(config.model_client),
        )

    def _get_system_message(self, scenario_type: ScenarioType) -> str:
        """Returns the system message for the given scenario type."""

        if scenario_type == ScenarioType.NEW_CODE or scenario_type == ScenarioType.NEW_APP:
            return self._system_message_new
        elif scenario_type == ScenarioType.MODIFY_CODE:
            return self._system_message_modify
        else:
            raise ValueError(f"System message not defined for the scenario type: {scenario_type}")

    def _get_tools(self, scenario_type: ScenarioType):
        """Returns the list of tools for the given scenario type."""

        if scenario_type == ScenarioType.NEW_CODE or scenario_type == ScenarioType.NEW_APP:
            return []
        elif scenario_type == ScenarioType.MODIFY_CODE:
            return [file_exists, read_file]
        else:
            raise ValueError(f"Tools not defined for the scenario type: {scenario_type}")

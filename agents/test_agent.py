import textwrap

from autogen_agentchat.agents import AssistantAgent, SocietyOfMindAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_core.models import ChatCompletionClient

from config import Config
from constants import TEST_AGENT_FAILED, TEST_AGENT_SUCCESSFUL
from tools.file_tools import enum_files, enum_subdirs, read_file, save_file
from tools.shell_tools import run_command


class TestAgent(SocietyOfMindAgent):
    """An agent that ensures the application's tests will pass."""

    _system_message = textwrap.dedent(
        f"""
        Your task is to ensure that all the tests of the application in the current directory will pass.
        
        You have an inner team to do the actual work, i.e. run the tests and fix the possible failed tests.
        """
    )

    _response_prompt = textwrap.dedent(
        f"""
        Respond either with '{TEST_AGENT_SUCCESSFUL}' or '{TEST_AGENT_FAILED}' according to the result from the inner team.
        Note that there may be failed tests in the conversation, so it is important to check the end result.
        """
    )

    _system_message_inner_test_agent = textwrap.dedent(
        f"""
        Your task is to run the tests of the appication in the current directory. If some tests fail, you should fix them to pass.
        Note that the application may consist of multiple components that are located in separate subdirectories.

        For each component, act as follows:
        - Find out the technology by investigating the file names and types in the component directory.
        - After detecting the component technology, determine the "run tests" command.
        - Run the tests.
        - Check the test results for failed tests.
        - If some tests fail, fix the failed tests.
        - If there are no tests for the component, skip the component.
        
        If you managed to fix all tests of the application, say '{TEST_AGENT_SUCCESSFUL}' without any other content.
        If you failed to fix some tests, say '{TEST_AGENT_FAILED}' without any other content.
        
        You have the following tools:
        - run_command tool running commands
        - read_file tool for reading files
        - save_file tool for saving files
        - enum_subdirs tool for enumerating subdirectories in a directory
        - enum_files tool for enumerating files in a directory
        """
    )

    # This is not a test class
    __test__ = False

    def __init__(self, config: Config):
        super().__init__(
            name="test_agent",
            model_client=ChatCompletionClient.load_component(config.model_client),
            instruction=self._system_message,
            response_prompt=self._response_prompt,
            team=TestAgent._create_team(config, self._system_message_inner_test_agent),
        )

    @staticmethod
    def _create_team(config: Config, system_message_inner_test_agent: str) -> RoundRobinGroupChat:
        """Creates an inner team."""

        inner_test_agent = AssistantAgent(
            name="inner_test_agent",
            system_message=system_message_inner_test_agent,
            model_client=ChatCompletionClient.load_component(config.model_client),
            tools=[run_command, read_file, save_file, enum_subdirs, enum_files],
        )
        termination_condition = TextMentionTermination(TEST_AGENT_SUCCESSFUL) or TextMentionTermination(
            TEST_AGENT_FAILED
        )
        team = RoundRobinGroupChat([inner_test_agent], termination_condition=termination_condition)
        return team

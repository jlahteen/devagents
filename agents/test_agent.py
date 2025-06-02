import textwrap
from typing import Sequence

from autogen_agentchat.agents import AssistantAgent, SocietyOfMindAgent
from autogen_agentchat.base import OrTerminationCondition
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.messages import AgentEvent, ChatMessage
from autogen_agentchat.teams import SelectorGroupChat
from autogen_core.models import ChatCompletionClient

from config import Config
from constants import TEST_AGENT_FAILED, TEST_AGENT_SUCCESSFUL
from tools.file_tools import delete_file, enum_files, enum_subdirs, read_file, save_file
from tools.shell_tools import run_command
from tools.web_tools import google_search, load_page

TEAM_LEAD_AGENT_NAME = "team_lead_agent"
TESTER_AGENT_NAME = "tester_agent"
ANALYST_AGENT_NAME = "analyst_agent"
FIXER_AGENT_NAME = "fixer_agent"
TESTER_AGENT_DONE = "TESTER_AGENT DONE"
FIXER_AGENT_DONE = "FIXER_AGENT DONE"


class TestAgent(SocietyOfMindAgent):
    """An agent that ensures the application's tests will pass."""

    _system_message = textwrap.dedent(
        f"""
        Your are a test agent that ensures all the tests of the application in the current directory will pass.
        
        You have an inner team to do the actual work, i.e. run the tests and fix the possible failed tests.
        """
    )

    _response_prompt = textwrap.dedent(
        f"""
        Respond either with '{TEST_AGENT_SUCCESSFUL}' or '{TEST_AGENT_FAILED}' according to the response from the inner team.
        """
    )

    _system_message_team_lead_agent = textwrap.dedent(
        f"""
        You run the team that tests the application in the current directory.

        Your task is to control how long the testing process will continue.
        Do not comment on the testing process or the results of the tests. There are other agents for that.
        
        The team runs on iterations. Each iteration goes as follows:
        - The tester agent runs the tests and reports the results.
        - The analyst agent analyzes the test results and suggests fixes for the failed tests.
        - The fixer agent implements the suggested fixes.

        When the iteration is done, check the test results and decide whether to continue or not.
        If you decide to take a new iteration, end your response with 'Please rerun the tests.'
        You should give up only in very rare circumstances where the fixes don't seem to work after several iterations.

        You should end the conversation in the following cases:
        - If there are no tests in the application, say '{TEST_AGENT_SUCCESSFUL}' without any other content.
        - If all tests passed, say '{TEST_AGENT_SUCCESSFUL}' without any other content.
        - If you feel the team is facing overwhelming obstacles fixing the tests, response with a short explanation why you
          decided to end the testing process. End your response with '{TEST_AGENT_FAILED}' in a separate line.
        """
    )

    _system_message_tester_agent = textwrap.dedent(
        f"""
        Your task is to run the tests of the application in the current directory.
        Always run the tests when your turn comes.
        Do not analyze or fix the failed tests, neither ask questions about failed tests, it is not your job.
        Just run the tests and report the results.
        
        Note that the application may consist of multiple components that are located in separate subdirectories.

        For each found component, run the tests as follows:
        - Find out the technology by investigating the files (names, types, contents) in the component directory.
        - After detecting the component technology, determine the "run tests" command.
        - Ensure that the testing framework is configured for CI/CD (e.g. no user input, no interactive prompts).
          - Especially for npm test use the "-- --ci --watchAll=false" options.
        - Run the tests.
        - If there are no tests for the component, do not suggest to add tests, just skip the component.

        When all tests are run, say '{TESTER_AGENT_DONE}' without any other content.
        
        You have the following tools:
        - run_command tool for running commands
        - read_file tool for reading files
        - enum_subdirs tool for enumerating subdirectories in a directory
        - enum_files tool for enumerating files in a directory
        """
    )

    _system_message_analyst_agent = textwrap.dedent(
        f"""
        Your task is to analyze the tests results and suggest fixes for the failed tests.
        
        Act as follows:
        - Use your knowledge to suggest fixes, but if that is not enough, use google_search and load_page tools
          to find the latest information about the errors.
        - Do not ask questions, just suggest specific fixes.
        - If there no tests found, do not suggest to add tests.

        You have the following tools:
        - read_file tool for reading files
        - enum_subdirs tool for enumerating subdirectories in a directory
        - enum_files tool for enumerating files in a directory
        - google_search tool for searching the web for latest information
        - load_page tool for loading a web page found by the google_search tool
        """
    )

    _system_message_fixer_agent = textwrap.dedent(
        f"""
        You are a developer. Your task is to fix the failed tests according to the suggested fixes.

        Do not comment on the suggested fixes, just implement them.
        Do not suggest new fixes, just implement the suggested ones.
        Do not run the tests, there is another agent for that.
        
        When you have implemented the suggested fixes or there is nothing to fix, say '{FIXER_AGENT_DONE}' without any other content.

        You have the following tools:
        - read_file tool for reading files
        - save_file tool for saving files
        - enum_subdirs tool for enumerating subdirectories in a directory
        - enum_files tool for enumerating files in a directory
        - delete_file tool for deleting files
        - run_command tool for running commands
        """
    )

    # This is not a test class even though its name starts with "test".
    __test__ = False

    def __init__(self, config: Config):
        super().__init__(
            name="test_agent",
            model_client=ChatCompletionClient.load_component(config.model_client),
            instruction=self._system_message,
            response_prompt=self._response_prompt,
            team=TestAgent._create_team(
                config,
                self._system_message_team_lead_agent,
                self._system_message_tester_agent,
                self._system_message_analyst_agent,
                self._system_message_fixer_agent,
            ),
        )

    @staticmethod
    def select_next_speaker(messages: Sequence[AgentEvent | ChatMessage]):
        if len(messages) == 1:
            return TESTER_AGENT_NAME
        elif messages[-1].source == TEAM_LEAD_AGENT_NAME:
            return TESTER_AGENT_NAME
        elif messages[-1].source == TESTER_AGENT_NAME:
            if TESTER_AGENT_DONE in messages[-1].content:
                return ANALYST_AGENT_NAME
            else:
                return TESTER_AGENT_NAME
        elif messages[-1].source == ANALYST_AGENT_NAME:
            return FIXER_AGENT_NAME
        elif messages[-1].source == FIXER_AGENT_NAME:
            if FIXER_AGENT_DONE in messages[-1].content:
                return TEAM_LEAD_AGENT_NAME
            else:
                return FIXER_AGENT_NAME
        else:
            # A jump into this agent from another agent, so let's start testing
            return TESTER_AGENT_NAME

    @staticmethod
    def _create_team(
        config: Config,
        system_message_team_lead_agent: str,
        system_message_tester_agent: str,
        system_message_analyst_agent: str,
        system_message_fixer_agent: str,
    ) -> SelectorGroupChat:
        """Creates an inner team."""

        model_client = ChatCompletionClient.load_component(config.model_client)
        team_lead_agent = AssistantAgent(
            name=TEAM_LEAD_AGENT_NAME,
            system_message=system_message_team_lead_agent,
            model_client=model_client,
        )
        tester_agent = AssistantAgent(
            name=TESTER_AGENT_NAME,
            system_message=system_message_tester_agent,
            model_client=model_client,
            tools=[run_command, read_file, enum_subdirs, enum_files],
        )
        analyst_agent = AssistantAgent(
            name=ANALYST_AGENT_NAME,
            system_message=system_message_analyst_agent,
            model_client=model_client,
            tools=[read_file, google_search, load_page, enum_subdirs, enum_files],
        )
        fixer_agent = AssistantAgent(
            name=FIXER_AGENT_NAME,
            system_message=system_message_fixer_agent,
            model_client=model_client,
            tools=[read_file, save_file, enum_subdirs, enum_files, delete_file, run_command],
        )
        termination_condition = OrTerminationCondition(
            TextMentionTermination(TEST_AGENT_SUCCESSFUL), TextMentionTermination(TEST_AGENT_FAILED)
        )
        team = SelectorGroupChat(
            [team_lead_agent, tester_agent, analyst_agent, fixer_agent],
            model_client=model_client,
            selector_func=TestAgent.select_next_speaker,
            termination_condition=termination_condition,
        )
        return team

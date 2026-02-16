import textwrap

from agent_platform.agent_base import AgentBase, Message
from agents.inner_team_agent import InnerTeamAgent
from monitoring.monitor import MonitorBase
from tools.file_tools import delete_file, enum_files, enum_subdirs, read_file, save_file
from tools.shell_tools import run_command
from tools.web_tools import google_search, load_page
from utils.config import Config
from utils.constants import TEST_AGENT_FAILED, TEST_AGENT_SUCCESSFUL

TEAM_LEAD_AGENT_NAME = "team_lead_agent"
TESTER_AGENT_NAME = "tester_agent"
ANALYST_AGENT_NAME = "analyst_agent"
FIXER_AGENT_NAME = "fixer_agent"
TESTER_AGENT_DONE = "TESTER_AGENT DONE"
FIXER_AGENT_DONE = "FIXER_AGENT DONE"
ALL_TESTS_PASSED = "ALL TESTS PASSED"


class TestAgent(InnerTeamAgent):
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
        ## ROLE
        You are a team lead agent managing a team that runs automated tests for the application in the current
        directory.

        ## TASK
        Your task is to control how long the testing process will continue.

        ## INSTRUCTIONS
        - The team runs on iterations. Each iteration goes as follows:
          - The tester agent runs the tests and reports the results.
          - The analyst agent analyzes the test results and suggests fixes for the failed tests.
          - The fixer agent implements the suggested fixes.
        - When the iteration is done, check the test results and decide whether to continue or not.
          If you decide to take a new iteration, end your response with 'Please rerun the tests.'
          Important: You should give up only in very rare circumstances where the fixes don't seem to resolve test
          errors after several iterations. Continue if there is still some progress, even if the progress is very slow.
        - You should end the conversation in the following cases:
          - If there are no tests in the application, say '{TEST_AGENT_SUCCESSFUL}' without any other content.
          - If all tests passed, say '{TEST_AGENT_SUCCESSFUL}' without any other content.
          - If you feel the team is facing overwhelming obstacles fixing the tests, respond with a short explanation
            why you decided to end the testing process. End your response with '{TEST_AGENT_FAILED}' in a separate
            line.

        ## CONSTRAINTS
        Do not comment on the testing process or the results of the tests. There are other agents for that.
        """
    )

    _system_message_tester_agent = textwrap.dedent(
        f"""
        ## ROLE
        You are an agent that can run automated tests for several technologies and frameworks.

        ## TASK
        Your task is to run all the tests implemented for the application in the current workspace.

        ## INSTRUCTIONS
        - Always run the tests when your turn comes.
        - The application may consist of multiple components so there might be several test sets to run.
        - When looking for tests, directory names containing terms like "test", "tests", "spec", etc. are good
          indicators of test components. Investigate files in such directories whether they contain tests.
        - For each found test set, run the tests as follows:
          - Find out the test technology by investigating the file names, types and contents in the test directory.
          - After detecting the test technology, determine the test command.
          - Ensure that the test command is suitable for CI/CD (e.g. no user input, no interactive prompts).
            - For "npm test": use the "-- --ci --watchAll=false" options.
          - For the verbosity level of the test commands, use minimal or normal verbosity to reduce output.
            - For "dotnet test": do not use the "--no-build" option - always build before running the tests.
            - For "maven": use the "--no-transfer-progress" option.
          - Run the tests with the determined test commands and options.
        - After running all the tests, report the results.
          - If no tests are found, report also that.
        - When all tests are run and the results are reported, say '{TESTER_AGENT_DONE}' without any other content.

        ## CONSTRAINTS
        - Do not analyze or fix the failed tests, neither ask questions about failed tests, it is not your job.
        - If no tests are found, do not suggest to add tests.

        ## TOOLS
        You have the following tools:
        - enum_subdirs tool for enumerating subdirectories in a directory
        - enum_files tool for enumerating files in a directory
        - run_command tool for running commands
        - read_file tool for reading files
        """
    )

    _system_message_analyst_agent = textwrap.dedent(
        f"""
        ## ROLE
        You are an analyst agent specialized in analyzing automated test results.

        ## TASK
        Your task is to analyze the tests results and suggest fixes for the failed tests.

        ## INSTRUCTIONS
        - Use your knowledge to suggest fixes, but if that is not enough, use google_search and load_page tools to find
          the latest information about the errors.
        - Investigate the code files related to the failed tests to understand better the context of the errors.
        - If all tests passed, end your response with '{ALL_TESTS_PASSED}'.

        ## CONSTRAINTS
        - Do not ask questions, just suggest specific fixes.
        - Do not implement the suggested fixes, there is another agent for that.
        - If no tests are found, do not suggest to add tests.

        ## TOOLS
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
        ## ROLE
        You are an experienced developer specialized in fixing failed tests.

        ## TASK
        Your task is to fix the failed tests according to the suggested fixes.

        ## INSTRUCTIONS
        - Check the last message from the analyst agent for suggested fixes.
        - Implement the suggested fixes.
        - When you have implemented the fixes, say '{FIXER_AGENT_DONE}' without any other content.
        - If there are no suggested fixes, say '{FIXER_AGENT_DONE}' without any other content.

        ## CONSTRAINTS
        - Do not comment the suggested fixes, just implement them.
        - Do not suggest new fixes, just implement the suggested ones.
        - Do not run the tests, there is another agent for that.

        ## TOOLS
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

    def __init__(self, config: Config, monitor: MonitorBase = None, on_error_callback: callable = None):
        super().__init__(
            name="test_agent",
            config=config,
            agents=self._create_team(config),
            speaker_selector=self._select_speaker,
            system_message=self._system_message,
            response_prompt=self._response_prompt,
            success_phrase=TEST_AGENT_SUCCESSFUL,
            failure_phrase=TEST_AGENT_FAILED,
            monitor=monitor,
            on_error_callback=on_error_callback,
        )

    def _create_team(self, config: Config) -> list[AgentBase]:
        """Creates the inner team as AgentBase instances."""

        return [
            AgentBase(
                name=TEAM_LEAD_AGENT_NAME,
                system_message=self._system_message_team_lead_agent,
                config=config,
            ),
            AgentBase(
                name=TESTER_AGENT_NAME,
                system_message=self._system_message_tester_agent,
                config=config,
                tools=[run_command, read_file, enum_subdirs, enum_files],
            ),
            AgentBase(
                name=ANALYST_AGENT_NAME,
                system_message=self._system_message_analyst_agent,
                config=config,
                tools=[read_file, google_search, load_page, enum_subdirs, enum_files],
            ),
            AgentBase(
                name=FIXER_AGENT_NAME,
                system_message=self._system_message_fixer_agent,
                config=config,
                tools=[read_file, save_file, enum_subdirs, enum_files, delete_file, run_command],
            ),
        ]

    def _select_speaker(self, message_count: int, last_message: Message) -> str:
        """Selects the next speaker based on the last message."""

        if message_count == 1:
            return self._over_to(TEAM_LEAD_AGENT_NAME)
        if last_message.source == TEAM_LEAD_AGENT_NAME:
            return self._over_to(TESTER_AGENT_NAME)
        elif last_message.source == TESTER_AGENT_NAME:
            if TESTER_AGENT_DONE in last_message.content:
                return self._over_to(ANALYST_AGENT_NAME)
            else:
                return self._over_to(TESTER_AGENT_NAME)
        elif last_message.source == ANALYST_AGENT_NAME:
            if ALL_TESTS_PASSED in last_message.content:
                return self._over_to(TEAM_LEAD_AGENT_NAME)
            else:
                return self._over_to(FIXER_AGENT_NAME)
        elif last_message.source == FIXER_AGENT_NAME:
            if FIXER_AGENT_DONE in last_message.content:
                return self._over_to(TEAM_LEAD_AGENT_NAME)
            else:
                return self._over_to(FIXER_AGENT_NAME)
        else:
            # A jump into this agent from another agent, so let's start testing
            return self._over_to(TESTER_AGENT_NAME)

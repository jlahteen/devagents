import textwrap

from autogen_agentchat.agents import AssistantAgent, SocietyOfMindAgent
from autogen_agentchat.base import OrTerminationCondition
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_core.models import ChatCompletionClient

from config import Config
from constants import BUILD_AGENT_FAILED, BUILD_AGENT_SUCCESSFUL
from tools.file_tools import delete_file, enum_files, enum_subdirs, read_file, save_file
from tools.shell_tools import run_command
from tools.web_tools import google_search, load_page


class BuildAgent(SocietyOfMindAgent):
    """An agent that ensures the application will build."""

    _system_message = textwrap.dedent(
        f"""
        Your task is to ensure that the application in the current directory will build successfully.
        
        You have an inner team to do the actual work, i.e. check the build and fix the possible build errors.
        """
    )

    _response_prompt = textwrap.dedent(
        f"""
        Respond either with '{BUILD_AGENT_SUCCESSFUL}' or '{BUILD_AGENT_FAILED}' according to the result from the inner team.
        Note:
        - There may be build errors in the conversation, so it is important to check the end result.
        - Do not treat build warnings as a failure.
        """
    )

    _system_message_inner_build_agent = textwrap.dedent(
        f"""
        Your task is to build the appication in the current directory. If the application does not build, you should fix it.
        Note that the application may consist of multiple components that are located in separate subdirectories.
        The application should already exist, so you should not create any new files or directories.
        However, when fixing the build errors, you may need to modify existing files or delete unnecessary files.
        Do not run the tests, it is not your task.

        For each component, act as follows:
        - Find out the technology by investigating the file names and types in the component directory
        - After detecting the component technology, determine the build command
        - Run the build command (debug mode is preferred)
        - Check the build output for errors
        - If the build fails, fix the build errors
        - When fixing the build errors:
          - Locate the errors in the code by the file references in the build output
          - Use your knowledge to fix the errors but if that is not enough, use google_search and load_page tools
            to find the latest information about the errors
          - When googling, use build error codes and messages as search queries
        
        If you managed to build the application, say '{BUILD_AGENT_SUCCESSFUL}' without any other content.
        You should do everything you can to build the application, but if you feel you are facing overwhelming obstacles and want to give up,
        say '{BUILD_AGENT_FAILED}' without any other content.
        
        You have the following tools:
        - run_command tool running commands
        - read_file tool for reading files
        - save_file tool for saving files
        - enum_subdirs tool for enumerating subdirectories in a directory
        - enum_files tool for enumerating files in a directory
        - delete_file tool for deleting files
        - google_search tool for searching the web for latest information
        - load_page tool for loading web pages found by the google_search tool
        """
    )

    def __init__(self, config: Config):
        super().__init__(
            name="build_agent",
            model_client=ChatCompletionClient.load_component(config.model_client),
            instruction=self._system_message,
            response_prompt=self._response_prompt,
            team=BuildAgent._create_team(config, self._system_message_inner_build_agent),
        )

    @staticmethod
    def _create_team(config: Config, system_message_inner_build_agent: str) -> RoundRobinGroupChat:
        """Creates an inner team."""

        inner_build_agent = AssistantAgent(
            name="inner_build_agent",
            system_message=system_message_inner_build_agent,
            model_client=ChatCompletionClient.load_component(config.model_client),
            tools=[run_command, read_file, save_file, enum_subdirs, enum_files, delete_file, google_search, load_page],
        )
        termination_condition = OrTerminationCondition(
            TextMentionTermination(BUILD_AGENT_SUCCESSFUL), TextMentionTermination(BUILD_AGENT_FAILED)
        )
        team = RoundRobinGroupChat([inner_build_agent], termination_condition=termination_condition)
        return team

import textwrap
from typing import Sequence

from autogen_agentchat.agents import AssistantAgent, SocietyOfMindAgent
from autogen_agentchat.base import OrTerminationCondition
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.messages import AgentEvent, ChatMessage
from autogen_agentchat.teams import SelectorGroupChat
from autogen_core.models import ChatCompletionClient

from agents.inner_team_agent import InnerTeamAgent
from config import Config
from constants import BUILD_AGENT_FAILED, BUILD_AGENT_SUCCESSFUL
from scenarios.orchestrator_agent_base import OrchestratorContext
from tools.file_tools import delete_file, enum_files, enum_subdirs, read_file, save_file
from tools.shell_tools import run_command
from tools.web_tools import google_search, load_page

TEAM_LEAD_AGENT_NAME = "team_lead_agent"
BUILDER_AGENT_NAME = "builder_agent"
ANALYST_AGENT_NAME = "analyst_agent"
FIXER_AGENT_NAME = "fixer_agent"
BUILDER_AGENT_DONE = "BUILDER_AGENT DONE"
FIXER_AGENT_DONE = "FIXER_AGENT DONE"
BUILD_SUCCEEDED = "BUILD SUCCEEDED"


class BuildAgent(InnerTeamAgent):
    """An agent that ensures the application will build."""

    _system_message = textwrap.dedent(
        f"""
        You are a build agent, and your task is to ensure that the application in the current directory will build successfully.
        
        You have an inner team to do the actual work, i.e. check the build results and fix the possible build errors.
        """
    )

    _response_prompt = textwrap.dedent(
        f"""
        Respond either with '{BUILD_AGENT_SUCCESSFUL}' or '{BUILD_AGENT_FAILED}' according to the response from the inner team.
        Note:
        - There may be build errors in the early conversation, so it is important to check the end result.
        - Do not treat build warnings as a failure.
        """
    )

    _system_message_team_lead_agent = textwrap.dedent(
        f"""
        You run the team that builds the application in the current directory.

        Your task is to control how long the build process will continue.
        Do not comment the build process or the build results. There are other agents for that.

        The team runs on iterations. Each iteration goes as follows:
        - The builder agent builds the application and reports the results.
        - The analyst agent analyzes the build results and suggests fixes for the build errors.
        - The fixer agent implements the suggested fixes.

        When the iteration is done, check the build results and decide whether to continue or not.
        If you decide to take a new iteration, end your response with 'Please rebuild the application.'
        You should give up only in very rare circumstances where the fixes don't seem to resolve build errors after several iterations.

        You should end the conversation in the following cases:
        - If there is no application to build, say '{BUILD_AGENT_SUCCESSFUL}' without any other content.
        - If the build was successful, say '{BUILD_AGENT_SUCCESSFUL}' without any other content.
        - If you feel the team is facing overwhelming obstacles fixing the build errors, response with a short explanation why you
          decided to end the build process. End your response with '{BUILD_AGENT_FAILED}' in a separate line.
        """
    )

    _system_message_builder_agent = textwrap.dedent(
        f"""
        Your task is to build the application in the current directory.
        Do not run tests, just build the application. Pass options to skip tests if the build command also runs them.
        Note that the application may consist of multiple components that are located in separate subdirectories.
        The application should already exist, so do not create any new files or directories.
        Always build the application when your turn comes.
        Do not analyze or fix the build errors, neither ask questions, it is not your job.
        Just build the application and report the results.

        For each found component, run the build as follows:
        - Find out the technology by investigating the files (names, types, contents) in the component directory.
        - After detecting the component technology, determine the build command; pass options to skip tests if necessary.
        - Run the build command (debug mode is preferred).
          Use options that are suitable for CI/CD (e.g. no user input, no interactive prompts).

        When the build has been run for all components, say '{BUILDER_AGENT_DONE}' without any other content.

        You have the following tools:
        - run_command tool for running commands
        - read_file tool for reading files
        - enum_subdirs tool for enumerating subdirectories in a directory
        - enum_files tool for enumerating files in a directory
        """
    )

    _system_message_analyst_agent = textwrap.dedent(
        f"""
        Your task is to analyze the build results and suggest fixes for the build errors.
        Build warnings are not in the scope of the task, so do not suggest fixes for them.

        Act as follows:
        - Use your knowledge to suggest fixes, but if that is not enough, use google_search and load_page tools
          to find the latest information about the errors.
          When googling, use build error codes and messages as search queries.
        - Do not ask questions, just suggest specific fixes.
        - If the build was successful, end your response with '{BUILD_SUCCEEDED}'.

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
        You are a developer. Your task is to fix the build errors according to the suggested fixes.

        Act as follows:
        - Check the last message from the analyst agent for suggested fixes.
        - Implement the suggested fixes.
        - When you have implemented the fixes, say '{FIXER_AGENT_DONE}' without any other content.
        - If there are no suggested fixes, say '{FIXER_AGENT_DONE}' without any other content.

        Important notes:
        - Do not comment the suggested fixes, just implement them.
        - Do not suggest new fixes, just implement the suggested ones.
        - Do not run the build, there is another agent for that.

        You have the following tools:
        - read_file tool for reading files
        - save_file tool for saving files
        - enum_subdirs tool for enumerating subdirectories in a directory
        - enum_files tool for enumerating files in a directory
        - delete_file tool for deleting files
        - run_command tool for running commands
        """
    )

    def __init__(self, config: Config, context: OrchestratorContext = None):
        super().__init__(
            name="build_agent",
            model_client=ChatCompletionClient.load_component(config.model_client),
            instruction=self._system_message,
            response_prompt=self._response_prompt,
            team=self._create_team(
                config,
                self._system_message_team_lead_agent,
                self._system_message_builder_agent,
                self._system_message_analyst_agent,
                self._system_message_fixer_agent,
            ),
            context=context,
        )

    def _select_next_speaker(self, messages: Sequence[AgentEvent | ChatMessage]):
        """Selects the next speaker based on the last speaker and message in the conversation."""

        if len(messages) == 1:
            return self._over_to(BUILDER_AGENT_NAME)
        elif messages[-1].source == TEAM_LEAD_AGENT_NAME:
            return self._over_to(BUILDER_AGENT_NAME)
        elif messages[-1].source == BUILDER_AGENT_NAME:
            if BUILDER_AGENT_DONE in messages[-1].content:
                return self._over_to(ANALYST_AGENT_NAME)
            else:
                return self._over_to(BUILDER_AGENT_NAME)
        elif messages[-1].source == ANALYST_AGENT_NAME:
            if BUILD_SUCCEEDED in messages[-1].content:
                return self._over_to(TEAM_LEAD_AGENT_NAME)
            else:
                return self._over_to(FIXER_AGENT_NAME)
        elif messages[-1].source == FIXER_AGENT_NAME:
            if FIXER_AGENT_DONE in messages[-1].content:
                return self._over_to(TEAM_LEAD_AGENT_NAME)
            else:
                return self._over_to(FIXER_AGENT_NAME)
        else:
            # A jump into this agent from another agent, so let's start building
            return self._over_to(BUILDER_AGENT_NAME)

    def _create_team(
        self,
        config: Config,
        system_message_team_lead_agent: str,
        system_message_builder_agent: str,
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
        builder_agent = AssistantAgent(
            name=BUILDER_AGENT_NAME,
            system_message=system_message_builder_agent,
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
            TextMentionTermination(BUILD_AGENT_SUCCESSFUL), TextMentionTermination(BUILD_AGENT_FAILED)
        )
        team = SelectorGroupChat(
            [team_lead_agent, builder_agent, analyst_agent, fixer_agent],
            model_client=model_client,
            selector_func=self._select_next_speaker,
            termination_condition=termination_condition,
        )
        return team

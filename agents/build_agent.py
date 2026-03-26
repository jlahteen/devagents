import textwrap

from agent_platform.agent_base import AgentBase, Message
from agent_platform.history_optimizer import IterationOptimizer
from agents.inner_team_agent import InnerTeamAgent
from agents.research_agent import research_web
from monitoring.monitor import MonitorBase
from tools.file_tools import delete_file, enum_files, enum_subdirs, read_file, save_file
from tools.shell_tools import run_command
from utils.config import Config
from utils.constants import BUILD_AGENT_FAILED, BUILD_AGENT_SUCCESSFUL, DEFAULT_MAX_HISTORY_ITERATIONS

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
        You are a build agent, and your task is to ensure that the application in the current directory will build
        successfully.

        You have an inner team to do the actual work, i.e. check the build results and fix the possible build errors.
        """
    )

    _response_prompt = textwrap.dedent(
        f"""
        Respond either with '{BUILD_AGENT_SUCCESSFUL}' or '{BUILD_AGENT_FAILED}' according to the response from the
        inner team.
        Note:
        - There may be build errors in the early conversation, so it is important to check the end result.
        - Do not treat build warnings as a failure.
        """
    )

    _system_message_team_lead_agent = textwrap.dedent(
        f"""
        ## ROLE
        You are a team lead agent managing a team that builds the application in the current directory.

        ## TASK
        Your task is to control how long the build process will continue.

        ## CONSTRAINTS
        - NEVER comment the build process or the build results.

        ## INSTRUCTIONS
        - The team runs on iterations. Each iteration goes as follows:
          - The builder agent builds the application and reports the results.
          - The analyst agent analyzes the build results and suggests fixes for the build errors.
          - The fixer agent implements the suggested fixes.
        - When the iteration is done, check the build results and decide whether to continue or not.
          If you decide to take a new iteration, end your response with 'Please rebuild the application.'
          Important: You should give up only in very rare circumstances where the fixes don't seem to resolve build
          errors after several iterations. Continue if there is still some progress, even if the progress is very slow.
        - You should end the conversation in the following cases:
          - If there is no application to build, say '{BUILD_AGENT_SUCCESSFUL}' without any other content.
          - If the build was successful, say '{BUILD_AGENT_SUCCESSFUL}' without any other content.
          - If you feel the team is facing overwhelming obstacles fixing the build errors, response with a short
            explanation why you decided to end the build process. End your response with '{BUILD_AGENT_FAILED}' in a
            separate line.
        """
    )

    _system_message_builder_agent = textwrap.dedent(
        f"""
        ## ROLE
        You are an agent that can run application builds for several technologies and frameworks.

        ## TASK
        Your task is to build the application in the current directory.

        ## CONSTRAINTS
        - NEVER analyze the build results.
        - NEVER suggest or implement fixes for build errors.
        - NEVER create any new files or directories.

        ## INSTRUCTIONS
        - Always build the application when your turn comes.
        - Note that the application may consist of multiple components that are located in separate subdirectories.
        - For each found component, run the build as follows:
          - Find out the technology by investigating the files (names, types, contents) in the component directory.
          - After detecting the component technology, determine the build command.
            - Pass options to skip tests if the build command also runs them.
            - Use such options that are suitable for CI/CD (e.g. no user input, no interactive prompts).
            - Use the Release build configuration if applicable.
            - For the verbosity level of the build commands, use options that suppress INFO level output if available.
              - For "maven": use the "--no-transfer-progress" option.
          - Run the build command.
        - After running all builds, say '{BUILDER_AGENT_DONE}' without any other content.

        ## TOOLS
        You have the following tools:
        - run_command tool for running commands
        - read_file tool for reading files
        - enum_subdirs tool for enumerating subdirectories in a directory
        - enum_files tool for enumerating files in a directory
        """
    )

    _system_message_analyst_agent = textwrap.dedent(
        f"""
        ## ROLE
        You are an analyst agent specialized in analyzing build results.

        ## TASK
        Your task is to analyze the build results and suggest fixes for the build errors.
        Build warnings are not in the scope of the task, so do not suggest fixes for them.

        ## CONSTRAINTS
        - NEVER ask questions, just suggest specific fixes.

        ## INSTRUCTIONS
        - Use your knowledge to suggest fixes, but if that is not enough, use the research_web tool to find the latest
          information about the build errors. Use build error codes and messages as research topics. Build errors are
          syntax errors, missing dependencies, incompatible versions, configuration issues, etc. Do not research
          business-related topics.
        - Read each necessary file only once. Analyze all errors from that file in a single pass without re-reading.
          Even with multiple errors, read the file once and provide fixes for all issues together.
        - If the build was successful, end your response with '{BUILD_SUCCEEDED}'.

        ## TOOLS
        You have the following tools:
        - read_file tool for reading files
        - enum_subdirs tool for enumerating subdirectories in a directory
        - enum_files tool for enumerating files in a directory
        - research_web tool for researching topics online and getting focused summaries
        """
    )

    _system_message_fixer_agent = textwrap.dedent(
        f"""
        ## ROLE
        You are an experienced developer specialized in fixing build errors.

        ## TASK
        Your task is to fix the build errors according to the suggested fixes.

        ## CONSTRAINTS
        - NEVER comment the suggested fixes, just implement them.
        - NEVER suggest new fixes, just implement the suggested ones.
        - NEVER run the build.

        ## INSTRUCTIONS
        - Check the last message from the analyst agent for suggested fixes.
        - Implement the suggested fixes.
        - When you have implemented the fixes, say '{FIXER_AGENT_DONE}' without any other content.
        - If there are no suggested fixes, say '{FIXER_AGENT_DONE}' without any other content.

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

    def __init__(self, config: Config, monitor: MonitorBase = None, on_error_callback: callable = None):
        history_optimizer = IterationOptimizer(
            team_lead_agent_name=TEAM_LEAD_AGENT_NAME, max_iterations=DEFAULT_MAX_HISTORY_ITERATIONS
        )
        super().__init__(
            name="build_agent",
            config=config,
            agents=self._create_team(config),
            speaker_selector=self._select_speaker,
            system_message=self._system_message,
            response_prompt=self._response_prompt,
            success_phrase=BUILD_AGENT_SUCCESSFUL,
            failure_phrase=BUILD_AGENT_FAILED,
            monitor=monitor,
            on_error_callback=on_error_callback,
            history_optimizer=history_optimizer,
            team_lead_agent_name=TEAM_LEAD_AGENT_NAME,
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
                name=BUILDER_AGENT_NAME,
                system_message=self._system_message_builder_agent,
                config=config,
                tools=[run_command, read_file, enum_subdirs, enum_files],
            ),
            AgentBase(
                name=ANALYST_AGENT_NAME,
                system_message=self._system_message_analyst_agent,
                config=config,
                tools=[read_file, research_web, enum_subdirs, enum_files],
            ),
            AgentBase(
                name=FIXER_AGENT_NAME,
                system_message=self._system_message_fixer_agent,
                config=config,
                tools=[read_file, save_file, enum_subdirs, enum_files, delete_file, run_command],
            ),
        ]

    def _select_speaker(self, message_count: int, last_message: Message | None) -> str:
        """Selects the next speaker based on the last message."""

        if message_count == 1:
            return self._over_to(TEAM_LEAD_AGENT_NAME)
        if last_message.source == TEAM_LEAD_AGENT_NAME:
            return self._over_to(BUILDER_AGENT_NAME)
        elif last_message.source == BUILDER_AGENT_NAME:
            if BUILDER_AGENT_DONE in last_message.content:
                return self._over_to(ANALYST_AGENT_NAME)
            else:
                return self._over_to(BUILDER_AGENT_NAME)
        elif last_message.source == ANALYST_AGENT_NAME:
            if BUILD_SUCCEEDED in last_message.content:
                return self._over_to(TEAM_LEAD_AGENT_NAME)
            else:
                return self._over_to(FIXER_AGENT_NAME)
        elif last_message.source == FIXER_AGENT_NAME:
            if FIXER_AGENT_DONE in last_message.content:
                return self._over_to(TEAM_LEAD_AGENT_NAME)
            else:
                return self._over_to(FIXER_AGENT_NAME)
        else:
            # A jump into this agent from another agent, so let's start building
            return self._over_to(BUILDER_AGENT_NAME)

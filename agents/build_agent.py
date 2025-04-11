import textwrap
from typing import Sequence

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import Response
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.messages import BaseChatMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_core import CancellationToken
from autogen_core.models import ChatCompletionClient

from config import Config
from tools.file_tools import enum_files, enum_subdirs, read_file, save_file
from tools.shell_tools import run_command

BUILD_AGENT_SUCCESSFUL = "BUILD_AGENT SUCCESSFUL"
BUILD_AGENT_FAILED = "BUILD_AGENT FAILED"


class BuildAgent(AssistantAgent):
    """An agent that ensures the application will build."""

    _system_message = textwrap.dedent(
        f"""
        Your task is to build the appication in the current directory. If the application does not build, you should fix it.
        Note that the application may consist of multiple components that are located in separate subdirectories.

        For each component, act as follows:
        - Find out the technology by investigating the file names and types in the component directory.
        - After detecting the component technology, determine the build command.
        - Run the build command.
        - Check the build output for errors.
        - If the build fails, fix the build errors.
        
        If you managed to build the application, say '{BUILD_AGENT_SUCCESSFUL}' without any other content.
        If you failed to fix the build errors, say '{BUILD_AGENT_FAILED}' without any other content.
        
        You have the following tools:
        - run_command tool running commands
        - read_file tool for reading files
        - save_file tool for saving files
        - enum_subdirs tool for enumerating subdirectories in a directory
        - enum_files tool for enumerating files in a directory
        """
    )

    def __init__(self, config: Config):
        super().__init__(
            name="build_agent",
            system_message=self._system_message,
            model_client=ChatCompletionClient.load_component(config.model_client),
        )

        self._inner_build_agent = AssistantAgent(
            name="inner_build_agent",
            system_message=self._system_message,
            model_client=ChatCompletionClient.load_component(config.model_client),
            tools=[run_command, read_file, save_file, enum_subdirs, enum_files],
        )

    async def on_messages(self, messages: Sequence[BaseChatMessage], cancellation_token: CancellationToken) -> Response:
        """Starts the inner agent as one agent team."""

        termination_condition = TextMentionTermination(BUILD_AGENT_SUCCESSFUL) or TextMentionTermination(
            BUILD_AGENT_FAILED
        )
        team = RoundRobinGroupChat(
            [self._inner_build_agent],
            termination_condition=termination_condition,
        )
        chat_message = await team.run(
            task="Build the application in the current directory.",
            cancellation_token=None,
        )
        return chat_message

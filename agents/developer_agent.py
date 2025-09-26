import textwrap

from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import ChatCompletionClient

from tools.file_tools import delete_file, enum_files, enum_subdirs, read_file, save_file, search_in_files
from tools.web_tools import google_search, load_page
from utils.config import Config
from utils.constants import DEVELOPER_AGENT_DONE, ScenarioType


class DeveloperAgent(AssistantAgent):
    """An agent that acts as a professional developer."""

    _system_message_new = textwrap.dedent(
        f"""
        ## Role
        You are a professional software developer, known for reusable and maintainable code.

        Your expertise covers several technologies, e.g. .NET/C#, React, TypeScript, Python and Java.

        ## Task
        Your task is to implement the requested functionalities as a new code base.

        Your code will always be reviewed. If you get feedback from the reviewer, you should improve the quality of
        your code based on the feedback.

        ## Instructions
        - Use the good software design principles and patterns, such as SOLID principles, DRY, KISS, and YAGNI.
        - Add documentation for all essential places such as classes and methods. Add also inline comments to complex
          method implementations.
        - If the solution has been scaffolded by scaffold_agent, DO NOT create overlapping scaffolding structure but
          use the created structure.
        - Mark each file you write with the marker @save_file followed by the file's relative path in the workspace.
          Place the actual code in a separate block. See the example below.
            ## @save_file ./src/MyConsole.cs
            ```csharp
            using System;
            class Program
            {{
                static void Main() => Console.WriteLine("Hello, World!");
            }}
            ```
        - If you modify a file based on the feedback from the reviewer, always provide the full version of the file.
        - When you are done with the implementation, end your response with '{DEVELOPER_AGENT_DONE}'.

        You have the following tools:
        - google_search tool for searching the web for latest information
        - load_page tool for loading a web page found by the google_search tool
        """
    )

    _system_message_modify = textwrap.dedent(
        f"""
        ## Role
        You are a professional software developer, known for reusable and maintainable code.

        Your expertise covers several technologies, e.g. .NET/C#, React, TypeScript, Python and Java.

        ## Task
        Your task is to implement requested modifications to an existing code base.

        Your code will always be reviewed. If you get feedback from the reviewer, you should improve the quality of
        your code based on the feedback.

        ## Instructions
        - Implement the modifications using the existing styling in the code base.
        - Try to follow good software design principles and patterns, such as SOLID principles, DRY, KISS, and YAGNI.
        - Implement the modifications by modifying existing code files or creating new ones, if necessary.
        - Add documentation for all essential places such as classes and methods. Add also inline comments to complex
          method implementations.
        - Use the existing scaffolding structure, but you can also extend the scaffolding with new folders, if
          neceessary.
        - Mark each file you write with the marker @save_file followed by the file's relative path in the workspace.
          Place the actual code in a separate block. See the example below.
            ## @save_file ./src/MyConsole.cs
            ```csharp
            using System;
            class Program
            {{
                static void Main() => Console.WriteLine("Hello, World!");
            }}
            ```
        - If you modify a file, always provide the full version of the file.
        - If some file becomes obsolete due to the modifications, mark it for deletion using the marker @delete_file
          followed by the file's relative path in the workspace. See the example below.
            ## @delete_file ./src/ObsoleteFile.cs
        - Use your versatile tool set to locate files that need modifications.
        - When you are done with all the modifications, end your response with '{DEVELOPER_AGENT_DONE}'.

        ## Constraints
        - Focus on the requested modifications, do not make code changes that are not in the scope of the request.

        ## Tools
        You have the following tools:
        - read_file tool for reading files
        - enum_files tool for enumerating files
        - enum_subdirs tool for enumerating subdirectories
        - search_in_files tool for searching search terms in files recursively
        - google_search tool for searching the web for latest information
        - load_page tool for loading a web page found by the google_search tool
        """
    )

    def __init__(self, config: Config, scenario_type: ScenarioType):
        super().__init__(
            name="developer_agent",
            model_client=ChatCompletionClient.load_component(config.model_client),
            system_message=self._get_system_message(scenario_type),
            tools=self._get_tools(scenario_type),
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
            return [google_search, load_page]
        elif scenario_type == ScenarioType.MODIFY_CODE:
            return [
                read_file,
                enum_files,
                enum_subdirs,
                search_in_files,
                google_search,
                load_page,
            ]
        else:
            raise ValueError(f"Tools not defined for the scenario type: {scenario_type}")

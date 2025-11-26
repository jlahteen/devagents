import textwrap

from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import ChatCompletionClient

from tools.file_tools import delete_file, save_file
from utils.config import Config
from utils.constants import OUTPUT_AGENT_DONE


class OutputAgent(AssistantAgent):
    """
    An agent that manages file saving and deletion based on the conversation history.
    """

    _system_message = textwrap.dedent(
        f"""
        ## ROLE
        You are an agent that manages file saving and deletion based on the conversation history.

        ## TASKS
        You have two tasks:
        1. Go through the conversation history and delete all files that are marked for deletion.
        2. Go through the conversation history and save all files that are marked for saving.
        It is important to do the tasks in the above order.

        ## INSTRUCTIONS
        - Identity the files to save by looking for the marker @save_file in the conversation history. The marker is
          followed by a relative file path in the workspace. The actual file content is given in a block following the
          marker row. Below is an example of a file marked for saving:
            ## @save_file ./src/MyConsole.cs
            ```csharp
            using System;
            class Program
            {{
                static void Main() => Console.WriteLine("Hello, World!");
            }}
        - There might be multiple versions of the same file to save. In these cases, you must save the latest version
          of the file.
        - Identify the files to delete by looking for the marker @delete_file in the conversation history. The marker
          is followed by a relative file path in the workspace. Below is an example of a file marked for deletion:
            ## @delete_file ./src/MyConsole.cs
        - When you have deleted and saved all files, end your response with '{OUTPUT_AGENT_DONE}'.

        ## TOOLS
        - save_file tool for saving files
        - delete_file tool for deleting files
        """
    )

    def __init__(self, config: Config):
        super().__init__(
            name="output_agent",
            system_message=self._system_message,
            model_client=ChatCompletionClient.load_component(config.model_client),
            tools=[save_file, delete_file],
        )

import textwrap
from config import Config
from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import ChatCompletionClient
from tools.file_tools import save_file
from tools.shell_tools import run_script


class OutputAgent(AssistantAgent):
    """
    An agent that runs a possible scaffold script and saves generated code to the corresponding
    files.
    """
    
    _system_message = textwrap.dedent(
        """
        Your tasks are the following, follow the task order:
        1.  If there is a script named "Scaffold Script", run the script with the run_script tool
            by passing the content of the script to the tool.
            If there is no scaffold script, skip this step.
        2.  Save all (both changed and unchanged) code files corresponding to their relative file
            paths.
        
        You have the following tools:
        -   save_file tool for saving files
        -   run_script tool for running scripts
        
        Finally, say TERMINATE.
        """
    )

    def __init__(self, config: Config):
        super().__init__(
            name="output_agent",
            system_message=self._system_message,
            model_client=ChatCompletionClient.load_component(config.model_client),
            tools=[save_file, run_script],
        )

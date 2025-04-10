import textwrap
from config import Config
from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import ChatCompletionClient
from tools.shell_tools import run_command


class ScaffoldAgent(AssistantAgent):
    """An agent that scaffolds a directory structure for the requested solution."""

    _system_message = textwrap.dedent(
        """
        Your task is to scaffold a directory structure for the requested solution.
        
        Use the current directory as the solution root so do not create a directory for the
        solution.
        
        Do not write code for the requested solution excluding necessary placeholder files.
        
        Place each project in a separate subfolder under the solution root.
        
        Scaffold the directory structure by using appropriate CLI commands.
        
        Run all necessary install commands when scaffolding the solution.
        
        Run the commands as Windows OS compatible commands.
        
        Run each command with the run_command tool.
        """
    )

    def __init__(self, config: Config):
        super().__init__(
            name="scaffold_agent",
            system_message=self._system_message,
            model_client=ChatCompletionClient.load_component(config.model_client),
            tools=[run_command],
        )

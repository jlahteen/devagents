import textwrap
from config import Config
from autogen import ConversableAgent
from tools.file_tools import save_file
from tools.shell_tools import run_script


class ScaffoldAgent(ConversableAgent):
    _system_message = textwrap.dedent(
        """
        Your task is to generate a script to scaffold the directory structure for the requested solution.
        Title the scaffold script as "Scaffold Script". Place the script in a separate script block following the title.
        Use the current directory "./" as the solution root so DO NOT create a directory for the solution in the scaffold script.
        DO NOT write code for the requested solution excluding necessary placeholder files that should be dummy.
        Place each project in a separate subfolder under the solution root.
        Prefer scaffolding the directory structure by using appropriate CLI commands in scaffold.bat.
        Include also necessary install commands in the scaffold script.
        Make sure that all the versions of packages and components are compatible with each other in the scaffold script.
        Write the scaffold script for Windows OS as a .bat file.
        """
    )

    def __init__(self, config: Config):
        super().__init__(
            name="scaffold_agent",
            system_message=self._system_message,
            llm_config=config.llm_config,
        )
        self._code_execution_config = False
        self._human_input = "NEVER"

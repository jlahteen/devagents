import textwrap
from config import Config
from autogen import ConversableAgent
from tools.file_tools import save_file
from tools.script_tools import run_script


class ScaffoldAgent(ConversableAgent):
    _system_message = textwrap.dedent(
        """
        Your task is to script the scaffolding structure for the requested solution in the scaffold.bat script.
        Title the scaffold script as "./scaffold.bat".
        Use the current directory "./" as the solution root so DO NOT create a directory for the solution in scaffold.bat.
        DO NOT write code for the requested solution excluding necessary placeholder files.
        Place each project in a separate subfolder under the solution root.
        Prefer scaffolding the directory structure by using appropriate tech stack commands in scaffold.bat.
        Include also necessary install commands in scaffold.bat.
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

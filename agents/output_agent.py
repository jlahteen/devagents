import textwrap
from config import Config
from autogen import ConversableAgent
from tools.file_tools import save_file
from tools.script_tools import run_script


class OutputAgent(ConversableAgent):
    _system_message = textwrap.dedent(
        """
        You get a conversation between a developer and a reviewer.
        
        When your turn comes, the reviewer has approved the code and scripts written by the developer.
        
        Your task is to save all script and code files according to the file paths specified in the conversation.
        
        First save all script files and run them. After that save all code files.
        
        Note that all file paths must be followed.
        
        You have the following tools:
        - save_file tool to save files
        - run_script tool to run scripts
        
        In the end, say TERMINATE.
        """
    )

    def __init__(self, config: Config):
        super().__init__(
            name="output_agent",
            system_message=self._system_message,
            llm_config=config.llm_config,
            is_termination_msg=self._is_termination_msg,
        )

        self._code_execution_config = False
        self._human_input = "NEVER"

        self._executor_agent = ConversableAgent(
            "_executor_agent",
            system_message="",
            llm_config=None,
            human_input_mode="NEVER",
            is_termination_msg=self._is_termination_msg,
        )

        self.register_for_llm(
            name="save_file",
            description="A tool that can save a content to a file.",
        )(save_file)

        self.register_for_llm(
            name="run_script",
            description="A tool that can run scripts.",
        )(run_script)

        self._executor_agent.register_for_execution("save_file")(save_file)

        self._executor_agent.register_for_execution("run_script")(run_script)

        prompt = (
            "Perform the tasks according your role in the following conversation:\n"
        )

        self.register_nested_chats(
            [
                {
                    "recipient": self._save_file_executor,
                    "message": lambda _1, messages, _2, _3: prompt
                    + (
                        messages[-2]["content"]
                        if len(messages) >= 2
                        else messages[-1]["content"]
                    ),
                    "summary_method": "last_msg",
                }
            ],
            lambda sender: sender not in [self._save_file_executor, self],
        )

    def _is_termination_msg(self, msg: dict) -> bool:
        return (
            msg != None
            and msg["content"] != None
            and "TERMINATE" in msg["content"].upper()
        )

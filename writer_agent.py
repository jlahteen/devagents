import autogen
from config import Config
from autogen import ConversableAgent
from tools import save_code_to_file


class WriterAgent(ConversableAgent):
    def __init__(self, config: Config):
        super().__init__(
            name="writer_agent",
            system_message=config.writer_agent_system_message,
            llm_config=config.llm_config,
            is_termination_msg=self.is_termination_msg,
        )

        self._code_execution_config = False
        self._human_input = "NEVER"

        self._save_file_executor = ConversableAgent(
            "_save_file_executor",
            system_message="""
            Your task is to save code blocks found in conversations to the corresponding file.
            You use the save_code_to_file tool for saving files.
            """,
            llm_config=config.llm_config,
            human_input_mode="NEVER",
        )

        self.register_for_llm(
            name="save_code_to_file", description="A tool that can save code to a file."
        )(save_code_to_file)

        self._save_file_executor.register_for_execution("save_code_to_file")(
            save_code_to_file
        )

        prompt = "Write the code block to the files in the following conversation:\n"

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

    def is_termination_msg(self, msg: dict) -> bool:
        return (
            msg != None
            and msg["content"] != None
            and "TERMINATE" in msg["content"].upper()
        )

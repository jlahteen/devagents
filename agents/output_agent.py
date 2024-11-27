import textwrap
from config import Config
from autogen import ConversableAgent
from tools.file_tools import save_code_to_file


class OutputAgent(ConversableAgent):
    _system_message = textwrap.dedent(
        """
        You get a conversation between a developer and a reviewer.
        When your turn comes, the reviewer has approved the code written by the developer.
        Your task is to save the APPROVED version of the code blocks to the files specified in the conversation.
        Note that the file names may include a directory part which must be followed.
        You use the save_code_to_file tool and _executor_agent agent to save files.
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

        self._save_file_executor = ConversableAgent(
            "_executor_agent",
            system_message="",
            llm_config=None,
            human_input_mode="NEVER",
            is_termination_msg=self._is_termination_msg,
        )

        self.register_for_llm(
            name="save_code_to_file",
            description="A tool that can save a code block to a file.",
        )(save_code_to_file)

        self._save_file_executor.register_for_execution("save_code_to_file")(
            save_code_to_file
        )

        prompt = "Write the code blocks in the following message to the corresponding files mentioned before each block:\n"

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

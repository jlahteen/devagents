import textwrap
from config import Config
from autogen import ConversableAgent
from tools.file_tools import save_file
from tools.shell_tools import run_script


class OutputAgent(ConversableAgent):
    _system_message = textwrap.dedent(
        """
        Your tasks are the following, follow the task order:
        1.  If there is a script named "Scaffold Script", run the script with the run_script tool
            by passing the content of the script to the tool.
            If there is no scaffold script, skip this step.
        2.  Save all (both changed and unchanged) code files corresponding to their relative file
            paths.
        
        You have the following tools:
        - save_file tool for saving files
        - run_script tool for running scripts
        
        Finally, say TERMINATE.
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
                    "recipient": self._executor_agent,
                    "message": lambda _1, messages, _2, _3: prompt
                    + self._find_scaffold_message(messages)
                    + (
                        messages[-2]["content"]
                        if len(messages) >= 2
                        else messages[-1]["content"]
                    ),
                    "summary_method": "last_msg",
                }
            ],
            lambda sender: sender not in [self._executor_agent, self],
        )

    def _is_termination_msg(self, msg: dict) -> bool:
        return (
            msg != None
            and msg["content"] != None
            and "TERMINATE" in msg["content"].upper()
        )

    def _find_scaffold_message(self, messages) -> str:
        for message in messages:
            if message["name"] == "scaffold_agent":
                return message["content"]
        return "\n"

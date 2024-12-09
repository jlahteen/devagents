import textwrap
from config import Config
from autogen import ConversableAgent


class ReviewerAgent(ConversableAgent):
    _system_message = textwrap.dedent(
        """
        You are a very experienced software architect, specialized in several technologies like
        .NET/C#, React, Python etc.
        
        You set the standards for the quality code.
        
        Your task is to review the code written by developer and make sure that code is written
        according best practice architecture standard. It is especially important ensure that the
        is production ready (exception handling and logging etc.).
        
        If you approve the code, which means there are no issues to be fixed or developed, simply
        say 'CODE APPROVED' without any other content or text formatting.
        
        If you do not approve the code, you should give constructive feedback and comments on how
        to make the code better. In this case, do not include 'CODE APPROVED' to your answer.
        """
    )

    def __init__(self, config: Config):
        super().__init__(
            name="reviewer_agent",
            system_message=self._system_message,
            llm_config=config.llm_config,
        )
        self._code_execution_config = False
        self._human_input = "NEVER"

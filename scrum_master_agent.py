from config import Config
from autogen import UserProxyAgent, ConversableAgent, GroupChat, GroupChatManager


class ScrumMasterAgent(ConversableAgent):
    def __init__(self, config: Config, developer_agent, reviewer_agent, writer_agent):
        super().__init__(
            name="scrum_master_agent",
            system_message="You are a ScrumMaster agent that manages the DevAgents team consisting of AI agents.",
            llm_config=config.llm_config,
        )
        self._code_execution_config = False
        self._human_input = "NEVER"
        self._config = config
        self._developer_agent = developer_agent
        self._reviewer_agent = reviewer_agent
        self._writer_agent = writer_agent


    def select_next_speaker(self, last_speaker, groupchat):
        if last_speaker is self._user_proxy_agent:
            return self._developer_agent
        elif last_speaker is self._developer_agent:
            return self._reviewer_agent
        elif last_speaker is self._reviewer_agent:
            if groupchat.messages[-1]["content"].rstrip('. *\n').endswith('CODE APPROVED'):
                return self._writer_agent
            else:
                return self._developer_agent
        else:
            return None
        
    def start_chat(self, coding_request):
        # Create a user proxy agent
        self._user_proxy_agent = UserProxyAgent(
            "user_proxy_agent", human_input_mode="NEVER", code_execution_config=False
        )
        self.groupchat = GroupChat(
            agents=[self._user_proxy_agent, self._developer_agent, self._reviewer_agent, self._writer_agent],
            speaker_selection_method=self.select_next_speaker,
            messages=[],
            max_round=self._config.max_rounds,
        )
        self.manager = GroupChatManager(
            groupchat=self.groupchat, llm_config=self._config.llm_config
        )
        chat_result = self._user_proxy_agent.initiate_chat(
            self.manager, message=coding_request
        )
        return chat_result

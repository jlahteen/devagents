from dotenv import load_dotenv
from hello import say_hello

# Load the environment variables
load_dotenv()

from config import Config
from scrum_master_agent import ScrumMasterAgent
from developer_agent import DeveloperAgent
from reviewer_agent import ReviewerAgent
from writer_agent import WriterAgent


def main():
    say_hello()

    # Create a Config instance
    config = Config()

    # Create necessary agents

    # Developer Agent
    developer_agent = DeveloperAgent(config=config)

    # Reviewer Agent
    reviewer_agent = ReviewerAgent(config=config)

    # Writer Agent
    writer_agent = WriterAgent(config=config)

    # Get the request from the user
    user_prompt = "Hey! This is a software team of AI agents. How could we help you?\n"
    coding_request = input(user_prompt)

    # Create a ScrumMaster agent
    scrum_master_agent = ScrumMasterAgent(
        config, developer_agent, reviewer_agent, writer_agent
    )

    # Pass the customer request to the master agent
    chat_result = scrum_master_agent.start_chat(coding_request)


if __name__ == "__main__":
    main()

import datetime
import os
import sys

from dotenv import load_dotenv
from hello import say_hello
from utils.coding_mode import start_coding_mode
from utils.coding_mode import stop_coding_mode

# Load the environment variables
load_dotenv()

from config import Config
from agents.scrum_master_agent import ScrumMasterAgent
from agents.developer_agent import DeveloperAgent
from agents.reviewer_agent import ReviewerAgent
from agents.output_agent import OutputAgent


def main():
    say_hello()

    # Create a Config instance
    config = Config()

    # Create the necessary agents

    # Developer Agent
    developer_agent = DeveloperAgent(config=config)

    # Reviewer Agent
    reviewer_agent = ReviewerAgent(config=config)

    # Output Agent
    output_agent = OutputAgent(config=config)

    # Create a ScrumMaster agent
    scrum_master_agent = ScrumMasterAgent(
        config, developer_agent, reviewer_agent, output_agent
    )

    # Get the prompt from the user
    prompt = get_prompt()

    # Start the coding mode
    start_coding_mode()

    # Redirect stdout
    redirect_stdout()

    # Pass the prompt to the ScrumMaster agent
    chat_result = scrum_master_agent.start_chat(prompt)

    # Restore stdout
    restore_stdout()

    # Stop the coding mode
    stop_coding_mode()


# Gets a prompt containing a coding task. The user can either enter a prompt
# or enter a file path containg a prompt. In the latter case the file content
# will be returned.
def get_prompt():
    user_input = input("Enter a prompt or a requirement file:\n")
    prompt = ""

    if os.path.isfile(user_input):
        # The input is a valid file path
        try:
            with open(user_input, "r", encoding="utf-8") as file:
                prompt = file.read()
        except FileNotFoundError:
            print("File was not found.")
            sys.exit(1)
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        # The input is a prompt
        prompt = user_input

    return prompt


# Redirects stdout to a trace file.
def redirect_stdout():
    trace_file = (
        os.getenv("TRACE_DIR")
        + "/trace-"
        + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        + ".md"
    )
    sys.stdout = open(trace_file, "w", encoding="utf-8")


# Restores stdout.
def restore_stdout():
    sys.stdout.close()
    sys.stdout = sys.__stdout__


if __name__ == "__main__":
    main()

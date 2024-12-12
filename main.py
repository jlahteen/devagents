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
from agents.team_lead_agent import TeamLeadAgent
from agents.scaffold_agent import ScaffoldAgent
from agents.developer_agent import DeveloperAgent
from agents.reviewer_agent import ReviewerAgent
from agents.output_agent import OutputAgent


def main():
    say_hello()

    # Create a Config instance
    config = Config()

    # Create the necessary agents

    # Scaffold Agent
    scaffold_agent = ScaffoldAgent(config=config)

    # Developer Agent
    developer_agent = DeveloperAgent(config=config)

    # Reviewer Agent
    reviewer_agent = ReviewerAgent(config=config)

    # Output Agent
    output_agent = OutputAgent(config=config)

    # Create a Team Lead Agent
    team_lead_agent = TeamLeadAgent(
        config, scaffold_agent, developer_agent, reviewer_agent, output_agent
    )

    # Get the prompt from the user
    prompt = get_prompt()

    # Set the workspace directory
    set_workspace_directory()

    # Start the coding mode
    start_coding_mode()

    # Redirect stdout
    redirect_stdout()

    # Pass the prompt to the Team Lead agent
    chat_result = team_lead_agent.start_chat(prompt)

    # Restore stdout
    restore_stdout()

    # Stop the coding mode
    stop_coding_mode()


# Gets a prompt containing a coding task. The user can either enter a prompt
# or enter a file path containg a prompt. In the latter case the file content
# will be returned.
def get_prompt():
    user_input = input("Enter a prompt or a prompt file:\n> ")
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


def set_workspace_directory():
    # Build the default directory
    default_dir = os.path.join(os.getcwd(), "output")

    # Ask for the workspace directory
    workspace_dir = (
        input(f"Enter the workspace directory [{default_dir}]:\n> ")
        or default_dir
    )

    # Check if the workspace directory exists
    if not os.path.exists(workspace_dir):
        print(f"Workspace directory '{workspace_dir}' does not exist.")
        sys.exit(1)

    # Change to the workspace directory
    os.chdir(workspace_dir)


if __name__ == "__main__":
    main()

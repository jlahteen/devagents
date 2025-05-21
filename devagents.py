import argparse
import asyncio
import datetime
import os
import sys

from hello import say_hello
from scenarios.scenario_base import create_scenario
from utils.coding_mode import start_coding_mode, stop_coding_mode


async def main():
    """The main program to run DevAgents."""

    # Start by saying Hello
    say_hello()

    # Parse the command line args
    args = parse_args()

    # Create a scenario
    scenario = create_scenario(args.scenario)

    # Get the prompt from the user
    prompt = get_prompt()

    # Set the workspace
    set_workspace(args.workspace)

    # Start the coding mode
    start_coding_mode()

    # Redirect stdout
    redirect_stdout()

    # Run the scenario
    await scenario.run_scenario(prompt=prompt)

    # Restore stdout
    restore_stdout()

    # Stop the coding mode
    stop_coding_mode()


def get_prompt():
    """
    Gets a prompt containing a coding task.

    The user can either enter a prompt or enter a file path containg a prompt.
    In the latter case the file content will be returned.
    """

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


def redirect_stdout():
    """Redirects stdout to a trace file."""

    trace_file = os.getenv("TRACE_DIR") + "/trace-" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".md"
    sys.stdout = open(trace_file, "w", encoding="utf-8")


def restore_stdout():
    """Restores stdout."""

    sys.stdout.close()
    sys.stdout = sys.__stdout__


def set_workspace(workspace=None):
    """Sets the workspace."""

    # Use the argument if provided, otherwise ask the user
    if not workspace:
        workspace = input(f"Enter the workspace:\n> ")

    # Check if the workspace exists
    if not os.path.exists(workspace):
        print(f"Workspace '{workspace}' does not exist.")
        sys.exit(1)

    # Change the current directory to the workspace
    os.chdir(workspace)


def parse_args():
    # Create a parser
    parser = argparse.ArgumentParser(description="DevAgents")

    # Add arguments
    parser.add_argument("--scenario", type=str, default=None, help="A scenario to run")
    parser.add_argument("--workspace", type=str, default=None, help="A directory specifying the workspace to use")

    # Parse the arguments
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    asyncio.run(main())

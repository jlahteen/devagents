import argparse
import asyncio
import datetime
import os
import sys

from hello import say_hello
from scenarios.scenario_base import create_scenario
from utils.misc import Tee, print_yellow


async def main():
    """The main program to run DevAgents."""

    print("\n** DevAgents **\n")

    # Parse the command line args
    args = parse_args()

    # Get the scenario
    scenario_name = get_scenario(args.scenario)

    # Create the scenario
    scenario = create_scenario(scenario_name)

    # Get the prompt
    prompt = get_prompt(args.prompt)

    # Set the workspace
    set_workspace(args.workspace)

    # Report the start time
    start_time = datetime.datetime.now().astimezone()
    print_yellow(f"\n** Coding task started at {start_time.strftime('%H.%M.%S')} **\n")

    # Redirect the console streams
    redirect_stdout_stderr()

    # Run the scenario
    await scenario.run_scenario(prompt=prompt)

    # Restore the console streams
    restore_stdout_stderr()

    # Report the end time and elapsed time
    end_time = datetime.datetime.now().astimezone()
    elapsed = end_time - start_time
    print_yellow(f"\n** Coding task finished at {end_time.strftime('%H.%M.%S')}, elapsed time {str(elapsed)[:-7]} **\n")


def get_prompt(prompt=None):
    """
    Gets a prompt containing a coding task.

    The user can either enter a prompt or enter a file path containg a prompt.
    In the latter case the file content will be returned.
    """

    if not prompt:
        prompt = input("Enter a prompt or a prompt file:\n> ")

    if os.path.isfile(prompt):
        # The prompt is a valid file path
        try:
            with open(prompt, "r", encoding="utf-8") as file:
                prompt = file.read()
        except FileNotFoundError:
            print("File was not found.")
            sys.exit(1)
        except Exception as e:
            print(f"An error occurred: {e}")

    return prompt


def get_scenario(scenario=None):
    """
    Gets the scenario to run. If not provided, asks the user.
    """

    if not scenario:
        scenario = input("Enter the scenario to run:\n> ")
    return scenario


def redirect_stdout_stderr():
    """Redirects stdout and stderr."""

    trace_file_path = os.getenv("TRACE_DIR") + "/trace-" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".md"
    trace_file = open(trace_file_path, "w", encoding="utf-8")
    sys.stdout = Tee(sys.stdout, trace_file)
    sys.stderr = Tee(sys.stderr, trace_file)


def restore_stdout_stderr():
    """Restores stdout and stderr."""

    sys.stdout.close()
    sys.stderr.close()
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__


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
    parser.add_argument(
        "--prompt",
        type=str,
        default=None,
        help="A prompt as a raw prompt or as a file path to a file containing a prompt",
    )
    parser.add_argument("--workspace", type=str, default=None, help="A directory specifying the workspace to use")

    # Parse the arguments
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    asyncio.run(main())

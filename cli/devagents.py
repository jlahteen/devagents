import argparse
import asyncio
import os
import sys
import traceback
from asyncio.exceptions import CancelledError

from scenario_engine.scenario_engine import ScenarioEngine
from scenario_engine.scenario_task import ScenarioTaskResult
from utils.misc import is_valid_file_path, print_green, print_red, print_yellow


async def main():
    """The CLI of DevAgents."""

    print("\n** DevAgents CLI **")

    # Parse the command line args
    args = parse_args()

    # Get the command line args
    scenario_name = get_scenario(args.scenario)
    prompt = get_prompt(args.prompt)
    workspace = get_workspace(args.workspace)
    # Run the scenario
    print("\nSetting up a team of agents to run your scenario...")
    scenario_engine = ScenarioEngine()
    result = await scenario_engine.run_scenario(scenario_name, prompt, workspace)
    print_scenario_task_result(result)


def get_prompt(prompt=None):
    """
    Gets a prompt.

    The user can either enter a prompt or enter a file path containg a prompt.
    In the latter case the file content will be returned.
    """

    if not prompt:
        prompt = input("\nEnter a prompt or a prompt file:\n> ")

    # Try to read as file if it's a valid path format
    if is_valid_file_path(prompt):
        try:
            with open(prompt, "r", encoding="utf-8") as file:
                prompt = file.read()
        except OSError as e:
            print_red(f"\nError: {e}\n")
            sys.exit(1)

    return prompt


def get_scenario(scenario=None):
    """Gets the scenario to run. If not provided, asks the user."""

    if not scenario:
        scenario = input("\nEnter the scenario to run:\n> ")
    return scenario


def get_workspace(workspace=None):
    """Gets the workspace. If not provided, asks the user."""

    if not workspace:
        workspace = input(f"\nEnter the workspace:\n> ")
    return workspace


def parse_args():
    """Parses command line arguments."""

    # Create a parser
    parser = argparse.ArgumentParser(description="DevAgents")

    # Add the arguments
    parser.add_argument("--scenario", type=str, default=None, help="A scenario to run")
    parser.add_argument(
        "--prompt",
        type=str,
        default=None,
        help="A prompt as a raw prompt or a file path to a file containing a prompt",
    )
    parser.add_argument("--workspace", type=str, default=None, help="A directory specifying the workspace to use")

    # Parse and return the arguments
    return parser.parse_args()


def print_scenario_task_result(result: ScenarioTaskResult) -> None:
    """Prints the scenario task result to the console."""

    print_yellow(f"\nScenario Task Result:")
    print_yellow(f"  Scenario    : {result.scenario_name}")
    print_yellow(f"  Started At  : {result.started_at}")
    print_yellow(f"  Finished At : {result.finished_at}")
    print_yellow(f"  Elapsed Time: {result.elapsed}")
    print_yellow(f"  Task ID     : {result.task_id}")
    print_yellow(f"  Workspace   : {result.workspace}")
    if result.errors:
        print_red("  Errors:")
        for error in result.errors:
            print_red(f"    - {error}")
    else:
        print_green("  No errors occurred in the scenario task.")
    print()


def print_exception(e):
    """Prints an exception to the console."""

    print_red(f"\n** Unhandled error **\n")
    print_red(f"{e}")
    print_red(traceback.format_exc())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, CancelledError):
        print_yellow("\n** Cancelled by the user **\n")
    except Exception as e:
        print_exception(e)

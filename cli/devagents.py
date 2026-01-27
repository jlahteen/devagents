import argparse
import asyncio
import os
import sys
import traceback
from asyncio.exceptions import CancelledError

from utils.misc import is_valid_file_path, print_green, print_red, print_yellow
from workflow_engine.workflow_engine import WorkflowEngine, WorkflowResult


async def main():
    """The CLI of DevAgents."""

    print("\n** DevAgents CLI **")

    # Parse the command line args
    args = parse_args()

    # Get the command line args
    workflow_name = get_workflow(args.workflow)
    prompt = get_prompt(args.prompt)
    workspace = get_workspace(args.workspace)
    # Run the workflow
    print("\nSetting up a team of agents to run your workflow...")
    workflow_engine = WorkflowEngine()
    result = await workflow_engine.run_workflow(workflow_name, prompt, workspace)
    print_workflow_result(result)


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


def get_workflow(workflow=None):
    """Gets the workflow to run. If not provided, asks the user."""

    if not workflow:
        workflow = input("\nEnter the workflow to run:\n> ")
    return workflow


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
    parser.add_argument("--workflow", type=str, default=None, help="A workflow to run")
    parser.add_argument(
        "--prompt",
        type=str,
        default=None,
        help="A prompt as a raw prompt or a file path to a file containing a prompt",
    )
    parser.add_argument("--workspace", type=str, default=None, help="A directory specifying the workspace to use")

    # Parse and return the arguments
    return parser.parse_args()


def print_workflow_result(result: WorkflowResult) -> None:
    """Prints the workflow result to the console."""

    print_yellow(f"\nWorkflow Result:")
    print_yellow(f"  Workflow    : {result.workflow_name}")
    print_yellow(f"  Started At  : {result.started_at}")
    print_yellow(f"  Finished At : {result.finished_at}")
    print_yellow(f"  Elapsed Time: {result.elapsed}")
    print_yellow(f"  Run ID      : {result.run_id}")
    print_yellow(f"  Workspace   : {result.workspace}")
    if result.errors:
        print_red("  Errors:")
        for error in result.errors:
            print_red(f"    - {error}")
    else:
        print_green("  No errors occurred in the workflow.")
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

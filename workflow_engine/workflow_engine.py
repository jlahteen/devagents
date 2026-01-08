import datetime

from workflow_engine.workflow_task import WorkflowTask, WorkflowResult


class WorkflowEngine:
    """An engine for running workflows."""

    async def run_scenario(self, scenario_name, prompt, workspace) -> WorkflowResult:
        """Runs a scenario with a given prompt in the specified workspace."""

        # Create a workflow task
        workflow_task = WorkflowTask(scenario_name, prompt, workspace)

        # Run the workflow task
        try:
            return await workflow_task.run()
        except Exception as e:
            return WorkflowResult(
                scenario_name=workflow_task.scenario_name,
                started_at=workflow_task.started_at,
                finished_at=workflow_task.finished_at if workflow_task.finished_at else datetime.datetime.now(),
                task_id=workflow_task.id,
                workspace=workflow_task.workspace,
                errors=[e],
            )

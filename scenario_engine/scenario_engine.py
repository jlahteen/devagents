from scenario_engine.scenario_task import ScenarioTask, ScenarioTaskResult
import datetime


class ScenarioEngine:
    """An engine for running scenarios."""

    async def run_scenario(self, scenario_name, prompt, workspace) -> ScenarioTaskResult:
        """Runs a scenario with a given prompt in the specified workspace."""

        # Create a scenario task
        scenario_task = ScenarioTask(scenario_name, prompt, workspace)

        # Run the scenario task
        try:
            return await scenario_task.run()
        except Exception as e:
            return ScenarioTaskResult(
                scenario_name=scenario_task.scenario_name,
                started_at=scenario_task.started_at,
                finished_at=scenario_task.finished_at if scenario_task.finished_at else datetime.datetime.now(),
                task_id=scenario_task.id,
                workspace=scenario_task.workspace,
                errors=[e],
            )

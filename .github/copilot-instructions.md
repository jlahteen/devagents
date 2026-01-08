# DevAgents AI Coding Instructions

## Project Overview
DevAgents is a multi-agent AI system built on Microsoft AutoGen for autonomous software development tasks. The system uses a scenario-based approach where specialized agents collaborate in teams to generate code, create applications, fix builds, and run tests.

## Architecture

### Core Component Hierarchy
```
ScenarioTask → ScenarioBase → OrchestratorAgent → InnerTeamAgent → AgentBase
```

**Key directories:**
- `scenarios/` - Scenario implementations (NewApp, ModifyApp, FixBuild, etc.)
- `agents/` - Specialized agents (BuildAgent, DeveloperAgent, TestAgent, etc.)
- `agent_platform/` - **Framework-agnostic abstraction layer** - provides public interfaces to decouple from AutoGen, enabling framework swaps without impacting agents/scenarios
- `scenario_engine/` - Task execution orchestration
- `tools/` - File, shell, and web tools for agent capabilities
- `monitoring/` - Console monitoring with ANSI support

### Framework Abstraction Layer
The `agent_platform/` provides framework-agnostic base classes (`AgentBase`, `InnerTeamAgentBase`) that hide AutoGen implementation details. Agents and scenarios only depend on these public interfaces, not AutoGen directly. This enables framework changes without rewriting higher layers.

### Agent Team Pattern
Agents are organized hierarchically. Complex agents (like `BuildAgent`) use `InnerTeamAgent` to manage sub-teams with specialized roles. Example from [build_agent.py](agents/build_agent.py):
```python
# BuildAgent has an inner team: team_lead → builder → analyst → fixer
# Communication uses keyword-based routing (e.g., "BUILDER_AGENT DONE")
```

### Scenario Workflow
1. **ScenarioTask** validates workspace, creates monitor/trace, changes to workspace directory
2. **OrchestratorAgent** manages agent sequence via `_select_next_speaker()` state machine
3. **Agents** use tools and communicate via AutoGen's message system
4. Results written to workspace, traces saved to `trace/` directory

## Critical Conventions

### Agent Communication
- Agents use **keyword signals** in responses to trigger workflow transitions (e.g., `DEVELOPER_AGENT_DONE`, `BUILD_AGENT_SUCCESSFUL`)
- Find all signals in [utils/constants.py](utils/constants.py)
- Never modify these keywords without updating all agents that check for them

### Configuration
- **All agents require Config object** - loads from `.env` (see [utils/config.py](utils/config.py))
- Required `.env` vars: `AZURE_MODEL`, `AZURE_API_KEY`, `AZURE_ENDPOINT`, `AZURE_DEPLOYMENT`, `AZURE_API_VERSION`, `MAX_TURNS`
- Optional: `GOOGLE_API_KEY`, `GOOGLE_CSE_ID` for web search tools

### Tool Pattern
Tools in `tools/` must return strings:
- Success: `"tool_name OK: description"` + console print
- Error: `"tool_name ERROR: description"`
- All file/shell operations use thread locks (`file_lock`) for safety
- See [file_tools.py](tools/file_tools.py) and [shell_tools.py](tools/shell_tools.py)

### Workspace Execution Context
- **ScenarioTask changes directory to workspace** - agents operate in `os.getcwd()`
- File paths in tools should be relative or absolute to workspace
- Workspace must exist before scenario starts (validated in [scenario_task.py](scenario_engine/scenario_task.py#L89))

## Development Workflows

### Running Scenarios
```bash
# Activate virtual environment first
venv\Scripts\activate

# Run scenario (interactive if args missing)
python -m cli.devagents --scenario NewApp --prompt "Create a calculator" --workspace ./output/test

# Docker aliases (if using container)
new-app, modify-app, fix-build, fix-tests, new-code, modify-code
```

### Running Tests
```bash
# All tests
python tests/run_tests.py

# Individual test file (uncomment in run_tests.py)
pytest -s tests/test_build_agent.py
```

### Adding a New Agent
1. Inherit from `AgentBase` (simple) or `InnerTeamAgent` (complex with sub-team)
2. Define system message with clear role, task, instructions, constraints sections
3. Provide tools list in constructor: `super().__init__(name, system_message, config, tools=[func1, func2])`
4. Tools automatically wrapped by abstraction layer (AutoGen implementation hidden in [agent_base.py](agent_platform/agent_base.py#L37))
5. **Never import AutoGen directly** - use `agent_platform` interfaces to maintain framework independence

### Adding a New Scenario
1. Create `scenarios/<scenario_name>/` directory
2. Implement `ScenarioBase` subclass (see [scenario_base.py](scenarios/scenario_base.py))
3. Implement `OrchestratorBase` subclass with `run_team()` and `_select_next_speaker()` logic
4. Register in `ScenarioBase.create_scenario()` match statement
5. See [fix_build_orchestrator_agent.py](scenarios/fix_build/fix_build_orchestrator_agent.py) for simple example

## Testing Patterns

- Tests use `pytest` with async support
- Fixtures prepare test workspaces with broken code to fix
- Tests validate agent outputs and file artifacts
- Example: [test_fix_build_scenario.py](tests/test_fix_build_scenario.py)

## Common Pitfalls

1. **Forgetting Config dependencies** - All agents need Config object passed to constructor
2. **Missing termination keywords** - Agents won't transition without exact keyword matches
3. **Directory context** - Remember ScenarioTask changes to workspace; paths are relative to it
4. **Tool return types** - Tools must return strings (AutoGen requirement for function tools)
5. **Thread safety** - Always use `file_lock` in tools for file/directory operations

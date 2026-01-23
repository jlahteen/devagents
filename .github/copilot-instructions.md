# DevAgents AI Coding Instructions

## Project Overview
DevAgents is a multi-agent AI system built on Microsoft AutoGen for autonomous software development tasks. The system uses a workflow-based approach where specialized agents collaborate in teams to generate code, create applications, fix builds, and run tests.

## Architecture

### Core Component Hierarchy
```
WorkflowEngine → WorkflowFactory → WorkflowBase → AgentTeam → AgentBase
                                              ↓
                                        InnerTeamAgentBase
```

**Key directories:**
- `workflows/` - Workflow implementations (NewApp, ModifyApp, FixBuild, etc.)
- `agents/` - Specialized agents (BuildAgent, DeveloperAgent, TestAgent, etc.)
- `agent_platform/` - **Framework-agnostic abstraction layer** - provides public interfaces to decouple from AutoGen, enabling framework swaps without impacting agents/workflows
- `workflow_engine/` - Task execution orchestration
- `tools/` - File, shell, and web tools for agent capabilities
- `monitoring/` - Console monitoring with ANSI support

### Framework Abstraction Layer
The `agent_platform/` provides framework-agnostic interfaces that decouple from AutoGen:
- **AgentBase** - Base class for all agents with tool wrapping, provides `run(prompt)` method for simple agents
- **InnerTeamAgentBase** - Base for agents managing sub-teams, provides `run_inner_team(prompt)` method
- **AgentTeam** - Wrapper around SelectorGroupChat with `run(prompt)` interface
- **MessageTermination** - Wrapper class for keyword-based termination conditions
- **SuccessOrFailureTermination** - Custom termination based on success/failure phrases with callback support

**Platform-agnostic means:**
- ✅ Internal implementations can use AutoGen classes
- ✅ Public methods/properties must not expose AutoGen types in signatures
- ✅ Use adapters/wrappers to convert between AutoGen types and platform-agnostic types (e.g., `SpeakerSelectorFunc`, `Message`)
- ❌ Never expose `AgentEvent`, `ChatMessage`, or other AutoGen-specific types in public APIs

Agents and workflows depend only on these interfaces, not AutoGen directly. This enables framework changes without rewriting higher layers.

### Agent Team Pattern
Agents are organized hierarchically. Complex agents (like `BuildAgent`) use `InnerTeamAgent` to manage sub-teams with specialized roles. Example from [build_agent.py](agents/build_agent.py):
```python
# BuildAgent has an inner team: team_lead → builder → analyst → fixer
# Communication uses keyword-based routing (e.g., "BUILDER_AGENT DONE")
```

### Workflow Execution Flow
1. **WorkflowEngine.run_workflow()** validates workspace, generates run_id, creates monitor/trace, changes to workspace directory
2. **WorkflowFactory** creates workflow instance based on workflow name
3. **WorkflowBase** subclasses implement `run(prompt)` method:
   - **AppWorkflowBase** - Uses AgentTeam for full-stack workflows (scaffold, dev, build, test)
   - **CodeWorkflowBase** - Uses AgentTeam for code-only workflows (developer, reviewer)
   - **Simple workflows** - Directly call `agent.run_inner_team(prompt)` for single-agent workflows
4. **Agents** use tools and communicate through framework-agnostic abstractions
5. Results returned as WorkflowResult with run_id, timestamps, errors
6. Traces saved to `<workspace>/.devagents/trace-<run_id>.md`

## Critical Conventions

### Agent Communication
- Agents use **keyword signals** in responses to trigger workflow transitions (e.g., `DEVELOPER_AGENT_DONE`, `BUILD_AGENT_SUCCESSFUL`)
- Find all signals in [utils/constants.py](utils/constants.py)
- Never modify these keywords without updating all agents that check for them

### Configuration
- **All agents require Config object** - loads from `.env` (see [utils/config.py](utils/config.py))
- Required `.env` vars: `AZURE_MODEL`, `AZURE_API_KEY`, `AZURE_ENDPOINT`, `AZURE_DEPLOYMENT`, `AZURE_API_VERSION`
- Optional: `GOOGLE_API_KEY`, `GOOGLE_CSE_ID` for web search tools
- Max conversation turns (999) is set internally in agent_platform layer

### Tool Pattern
Tools in `tools/` must return strings:
- Success: `"tool_name OK: description"` + console print
- Error: `"tool_name ERROR: description"`
- All file/shell operations use thread locks (`file_lock`) for safety
- See [file_tools.py](tools/file_tools.py) and [shell_tools.py](tools/shell_tools.py)

### Workspace Execution Context
- **WorkflowEngine changes directory to workspace** - agents operate in `os.getcwd()`
- File paths in tools should be relative or absolute to workspace
- Workspace must exist before workflow starts (validated in [workflow_engine.py](workflow_engine/workflow_engine.py))
- Traces saved to `<workspace>/.devagents/trace-<run_id>.md` for debugging
- `.devagents` directory automatically excluded from file search operations

## Development Workflows

### Environment Setup
```bash
# Create virtual environment (first time only)
python -m venv ./venv

# Activate virtual environment (Windows)
venv\Scripts\activate
# Or use convenience script: _venv.ps1 (points to ag_0.4\Scripts\activate.ps1)

# Install dependencies
pip install -r requirements.txt

# Create .env file with required config (see Configuration section)
```

### Running Workflows
```bash
# Activate virtual environment first
venv\Scripts\activate

# Run workflow (interactive if args missing)
python -m cli.devagents --workflow NewApp --prompt "Create a calculator" --workspace ./output/test

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

### Debugging with VS Code
Launch configurations available in `.vscode/launch.json`:
- Run all workflows with debugger attached
- Module: `cli.devagents` with args `--workflow`, `--prompt`, `--workspace`

### Adding a New Agent
1. Inherit from `AgentBase` (simple) or `InnerTeamAgentBase` (complex with sub-team)
2. Define system message with clear role, task, instructions, constraints sections
3. Provide tools list in constructor: `super().__init__(name, system_message, config, tools=[func1, func2])`
4. For inner team agents, accept `monitor` and `on_error_callback` parameters for workflow integration
5. Tools automatically wrapped by abstraction layer (AutoGen implementation hidden in [agent_base.py](agent_platform/agent_base.py))
6. **Never import AutoGen directly** - use `agent_platform` interfaces to maintain framework independence

### Adding a New Workflow
1. Create `workflows/<workflow_name>/` directory with single workflow file (no separate orchestrator)
2. Implement `WorkflowBase` subclass with `run(prompt)` method
3. Choose appropriate base class:
   - **AppWorkflowBase** - For full-stack workflows (scaffold/build/test), uses AgentTeam with state machine
   - **CodeWorkflowBase** - For code-only workflows (dev/review), uses AgentTeam
   - **WorkflowBase** - For simple single-agent workflows, directly call `agent.run_inner_team(prompt)`
4. Constructor must accept `config: Config` and `monitor: MonitorBase` parameters
5. Register in `WorkflowFactory.create_workflow()` match statement
6. See [fix_build_workflow.py](workflows/fix_build/fix_build_workflow.py) for simple example

## Testing Patterns

- Tests use `pytest` with async support
- Fixtures prepare test workspaces with broken code to fix
- Tests validate agent outputs and file artifacts
- Example: [test_fix_build_workflow.py](tests/test_fix_build_workflow.py)
- **All tests use platform-agnostic APIs** - no direct AutoGen imports in test code
- Simple agents tested with `agent.run(prompt)` method
- Inner team agents tested with `agent.run_inner_team(prompt)` method
- Workflows tested with `workflow.run(prompt)` or via `WorkflowEngine.run_workflow()`
- Tests directly instantiate workflow classes: `workflow = FixBuildWorkflow(config=Config(), monitor=ConsoleMonitorAnsi())`
- Test workspaces created in `tests/test_output/` (temporary directories)

## Monitoring and Debugging

- Console monitor uses ANSI escape codes for real-time agent updates ([console_monitor_ansi.py](monitoring/console_monitor_ansi.py))
- Monitor shows current agent, elapsed time, and spinner animation in fixed bottom status line
- All agent communication traced to workspace `.devagents/trace-<run_id>.md` files
- Traces contain complete conversation history for post-mortem analysis

## Common Pitfalls

1. **Forgetting Config and Monitor dependencies** - All workflows need Config and MonitorBase; inner team agents need monitor and on_error_callback
2. **Missing termination keywords** - Agents won't transition without exact keyword matches from constants.py
3. **Directory context** - Remember WorkflowEngine changes to workspace; paths are relative to it
4. **Tool return types** - Tools must return strings (AutoGen requirement for function tools)
5. **Thread safety** - Always use `file_lock` in tools for file/directory operations
6. **Direct AutoGen imports** - Never import AutoGen classes in workflows, agents, or tests; use agent_platform abstractions
7. **Method naming** - Simple agents use `run(prompt)`, inner team agents use `run_inner_team(prompt)`, workflows use `run(prompt)`, AgentTeam uses `run(prompt)`
8. **Platform-agnostic types** - Use `SpeakerSelectorFunc`, `Message`, `MessageTermination` instead of AutoGen types in public APIs

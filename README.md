# DevAgents

DevAgents is an **experimental** project for using a team of AI agents to generate code for different scenarios.

The currently supported scenarios are:
- NewCode: A scenario for generating one or more code snippets e.g. specific classes, modules, scripts etc.
- NewApp: A scenario for generating complete applications. In this scenario applications should consists of a maximum of 5 components or services.

DevAgents is built on top of [Microsoft AutoGen](https://github.com/microsoft/autogen), a framework for creating AI-driven workflows.


## Local Setup

Follow these steps to set up DevAgents locally:

### 1. Create a Virtual Environment

Run the following commands in the terminal:

```bash
# Create a virtual Python environment
python -m venv ./venv

# Activate the virtual environment
venv\Scripts\activate

# Install the requirements
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Set the following environment variables in a `.env` file located in the root directory:

```
TRACE_DIR=<directory path for saving trace files>
MAX_TURNS=<mamimum number of turns in conversations>
MODEL=<LLM model name>
API_KEY=<API key for LLM calls>
AZURE_ENDPOINT=<Azure OpenAI endpoint to use>
AZURE_DEPLOYMENT=<Azure OpenAI model deployment name>
API_VERSION=<API version to use>
```

These variables are required to connect to your Azure OpenAI Service instance.

### 3. Run DevAgents

To start DevAgents, use the following command:

```bash
python devagents.py --scenario <ScenarioName>
```

When DevAgents starts, you will be asked to enter a prompt and a workspace directory. You can give a prompt as a raw prompt or as a file path to a file containing a prompt.


## Output

Generated code and other artifacts are saved in the given workspace directory.


## License

This project is licensed under the MIT License. See the `LICENSE` file for details.


## Remarks

DevAgents is currently tested only on Windows with Azure OpenAI Service.


## Example Run

Below is a sample output of running a NewApp scenario.

```bash
PS C:\_dev2\devagents> python devagents.py --scenario NewApp
====================================================
/  ____              _                    _        \
/ |  _ \  _____   __/ \   __ _  ___ _ __ | |_ ___  \
/ | | | |/ _ \ \ / / _ \ / _` |/ _ \ '_ \| __/ __| \
/ | |_| |  __/\ V / ___ \ (_| |  __/ | | | |_\__ \ \
/ |____/ \___| \_/_/   \_\__, |\___|_| |_|\__|___/ \
/                        |___/                     \
====================================================
 ✨  Hey! We are a software team of AI agents.  ✨
 ✨       Let's build something together!       ✨

Enter a prompt or a prompt file:
> my-simple-console-calculator.txt
Enter the workspace directory [C:\_dev2\devagents\output]:
> C:\_dev2\devagents\output\my-simple-console-calculator
Coding... Done
PS C:\_dev2\devagents> 
```

---
Happy coding with DevAgents! 🚀

---

## Backlog

- New: Add NewSystem scenario
- New: Add NewFeature scenario
- New: Add FixBuild scenario with a BuildAgent
- Bug: If a prompt file is not found, DevAgents starts to hallucinate
- New: Pass workspace directory as an argument
- New: Pass prompt as an argument
- New: Implment TestAgent run and fix tests

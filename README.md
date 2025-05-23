# DevAgents

DevAgents is an **experimental** project for using a team of AI agents to generate code for different scenarios.

The currently supported scenarios are listed in the table below.

| **Scenario**      | **Description**                                                                                     |
|-------------------|-----------------------------------------------------------------------------------------------------|
| NewCode           | A scenario for generating one or more code snippets, e.g., specific classes, modules, scripts, etc.|
| NewApp            | A scenario for generating complete applications. Applications should consist of a maximum of 5 components or services.|
| FixBuild          | A scenario to ensure an application builds successfully. Build errors will be fixed if necessary. |
| FixTests          | A scenario to ensure all tests pass successfully. Tests will be fixed if necessary. |

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
AZURE_MODEL=<Azure LLM model name>
AZURE_API_KEY=<Azure API key for LLM calls>
AZURE_ENDPOINT=<Azure OpenAI endpoint to use>
AZURE_DEPLOYMENT=<Azure OpenAI model deployment name>
AZURE_API_VERSION=<Azure API version to use>
GOOGLE_API_KEY = <Google API key>
GOOGLE_CSE_ID = "<Google Custom Search Engine ID>"
```

These variables are required to connect to your Azure OpenAI Service instance.

### 3. Run DevAgents

To start DevAgents, use the following command:

```bash
python devagents.py [--scenario <scenarioName>] [--prompt <prompt>] [--workspace <workspace>]
```

When DevAgents starts, you will be asked to enter missing command line arguments. You can give a prompt as a raw prompt or as a file path to a file containing a prompt. A workspace is a directory where DevAgents operates when processing a coding task specified by the given prompt.


## Output

Generated or modified code and other artifacts are saved in the given workspace.


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

Enter the scenario to run:
> NewApp
Enter a prompt or a prompt file:
> my-simple-console-calculator.txt
Enter the workspace:
> C:\_dev2\devagents\output\my-simple-console-calculator
Coding... Done
PS C:\_dev2\devagents> 
```

---
Happy prompting with DevAgents! 🚀

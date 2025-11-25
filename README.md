# Welcome to DevAgents!

DevAgents is an **experimental** project for using a team of AI agents for generating code or even create complete applications.

DevAgents uses a scenario-based approach. There are scenarios for different development tasks. DevAgents aims to complete all scenarios autonomously.

The scenarios, that are currently supported, are listed in the table below.

| **Scenario**      | **Description**                                                                                     |
|-------------------|-----------------------------------------------------------------------------------------------------|
| NewCode           | A scenario for generating one or more code files, e.g., specific classes, modules, scripts, etc.|
| ModifyCode        | A scenario for modifying one or more code files, e.g., specific classes, modules, scripts, etc.|
| NewApp            | A scenario for generating complete applications. In a NewApp scenario, the application will be built and tested by specialized agents. In this scenario, LLM context size is the only limitation for an application to create. |
| ModifyApp         | A scenario for modifying existing applications. In a ModifyApp scenario, the application will be rebuilt and retested after modifications by specialized agents. |
| FixBuild          | A scenario to ensure an application builds successfully. Build errors will be fixed if necessary. |
| FixTests          | A scenario to ensure all tests pass successfully. Tests will be fixed if necessary. |

DevAgents is built on top of [Microsoft AutoGen](https://github.com/microsoft/autogen), a framework for creating AI-driven workflows.


## DevAgents Architecture

DevAgents architecture is illustrated in the diagram below.

![DevAgents Logo](docs/devagents-architecture.png)


## How to Run Scenarios with DevAgents

To run scenarios with DevAgents, use the following command:

```bash
python -m cli.devagents.py [--scenario <scenarioName>] [--prompt <prompt>] [--workspace <workspace>]
```

When DevAgents starts, you will be asked to enter missing command line arguments. You can give a prompt as a raw prompt or as a file path to a file containing a prompt. A workspace is a directory where DevAgents operates when processing a coding task specified by the given prompt.

Generated or modified code and other artifacts are saved in the given workspace.

DevAgents is available in a Docker container. The container defines the following aliases for starting scenarios more easily.

| **Alias**   | **Definition**                       | **Description**              |
|-------------|--------------------------------------|------------------------------|
| devagents   | python -m cli.devagents              | Starts DevAgents             |
| new-code    | devagents --scenario NewCode         | Starts a NewCode scenario    |
| modify-code | devagents --scenario ModifyCode      | Starts a ModifyCode scenario |
| new-app     | devagents --scenario NewApp          | Starts a NewApp scenario     |
| modify-app  | devagents --scenario ModifyApp       | Starts a ModifyApp scenario  |
| fix-build   | devagents --scenario FixBuild        | Starts a FixBuild scenario   |
| fix-tests   | devagents --scenario FixTests        | Starts a FixTests scenario   |
| ver         | python -m cli.hello                  | Prints the DevAgents version |


## Configuration

To run DevAgents, you have to set the following environment variables in a `.env` file.

| Environment variable | Description                                                                                     |
|----------------------|-------------------------------------------------------------------------------------------------|
| AZURE_MODEL          | Azure LLM model name                                                                            |
| AZURE_API_KEY        | Azure API key for LLM calls                                                                     |
| AZURE_ENDPOINT       | Azure OpenAI endpoint to use                                                                    |
| AZURE_DEPLOYMENT     | Azure OpenAI model deployment name                                                              |
| AZURE_API_VERSION    | Azure API version to use                                                                        |
| MAX_TURNS            | Maximum number of turns in conversations                                                        |
| GOOGLE_API_KEY       | Google API key (optional, if not given, real time google searches are not available for agents) |
| GOOGLE_CSE_ID        | Google Custom Search Engine ID (optional, see above)                                            |

Below is a sample of a content of a `.env` file.

```bash
AZURE_MODEL=gpt-4.1
AZURE_ENDPOINT=https://<your-openai-name>.openai.azure.com/
AZURE_API_KEY=35RpgJ******************************************************************************
AZURE_DEPLOYMENT=gpt-41
AZURE_API_VERSION=2024-12-01-preview
MAX_TURNS=999
GOOGLE_API_KEY=AIza***********************************
GOOGLE_CSE_ID=3fc2************
```


## License

This project is licensed under the MIT License. See the `LICENSE` file for details.


## Remarks

- DevAgents is currently tested with Azure OpenAI Service using GPT-4o and GPT-4.1.
- Always carefully review and test all code written by AI - this is valid for all tools, not just DevAgents.


## Further Information

- [Local Development Setup](docs/local_dev_setup.md)


---
Happy prompting with DevAgents! 🚀

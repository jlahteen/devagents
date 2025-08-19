# Local Development Setup

Follow the steps below to setup DevAgents locally:

## Install Python

[Install Python](https://www.python.org/downloads/) 3.11 or later.

## Clone the DevAgents repository

Create a local development directory and clone the DevAgents repository.

```bash
# Create a local dev directory
mkdir <your-dev-directory>

# Move to the directory
cd <your-dev-directory>

# Clone the repository
git clone https://github.com/jlahteen/devagents
```

## Create a Virtual Environment

Create a virtual environment in the `devgents` directory:

```bash
# Move to devagents
cd devagents

# Create a virtual environment
python -m venv ./venv

# Activate the virtual environment
venv\Scripts\activate

# Install the requirements
pip install -r requirements.txt
```

## Configure Environment Variables

Create a `.env` file in the `devagents` directory to setup the configuration as instructed in the `README` file.

## Run DevAgents

To start DevAgents, use the following command:

```bash
python -m cli.devagents.py [--scenario <scenarioName>] [--prompt <prompt>] [--workspace <workspace>]
```

---
Happy prompting with DevAgents! 🚀

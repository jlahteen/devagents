# DevAgents
DevAgents is a POC project for AI agent based code generation using Microsoft AutoGen.

## Local Setup

Run the following commands in the terminal:
```python
# Create a virtual Python environment
python -m venv ./venv

# Activate the virtual environment
venv/scripts/activate

# Install the requirements
pip install -r requirements.txt
```

Set the following environment variables in the `.env` file:

```
AZURE_OPENAI_KEY=<AZURE_OPENAI_KEY>
AZURE_OPENAI_URL=<AZURE_OPENAI_URL>
AZURE_GPT_DEPLOYMENT_NAME=<AZURE_GPT_DEPLOYMENT_NAME>
```

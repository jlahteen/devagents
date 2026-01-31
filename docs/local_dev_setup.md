# Local Development Setup

Follow the steps below to set up DevAgents locally:

## 1. Install Python

- [Install Python](https://www.python.org/downloads/) 3.11 or later.

## 2. Clone the DevAgents Repository

Create a local development directory and clone the DevAgents repository:

```powershell
# Create a local dev directory
mkdir <your-dev-directory>
cd <your-dev-directory>

# Clone the repository
git clone https://github.com/jlahteen/devagents
cd devagents
```

## 3. Create and Activate a Virtual Environment

Create a virtual environment:

```powershell
# Create a virtual environment
python -m venv ./venv

# Activate the virtual environment
.\venv\Scripts\Activate.ps1
```

## 4. Install Requirements

Install dependencies from the provided requirements.txt:

```powershell
pip install -r requirements.txt
```

## 5. Configure Environment Variables

Create a `.env` file in the `devagents` directory to set up configuration as instructed in the `README` file.

## 6. Run DevAgents

Activate your virtual environment if not already active, then run:

```powershell
python -m cli.devagents --workflow <workflowName> --prompt "<prompt>" --workspace <workspace>
```

## 7. Troubleshooting

- If you encounter dependency issues, run:
  ```powershell
  pip check
  ```
- If you accidentally overwrite requirements.txt, restore it from version control and reinstall:
  ```powershell
  git checkout requirements.txt
  pip install -r requirements.txt
  ```

---
Happy prompting with DevAgents! 🚀

# DevAgents Developer Guide

Welcome to the **DevAgents** developer guide!  
This guide covers everything you need to set up, maintain, and develop with DevAgents.

---

## 🚀 Getting Started

### 1. Install Python

- [Install Python](https://www.python.org/downloads/) 3.11 or later.

### 2. Clone the DevAgents Repository

Create a local development directory and clone the DevAgents repository:

```powershell
# Create a local dev directory
mkdir <your-dev-directory>
cd <your-dev-directory>

# Clone the repository
git clone https://github.com/jlahteen/devagents
cd devagents
```

### 3. Create and Activate a Virtual Environment

Create a virtual environment:

```powershell
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
.\.venv\Scripts\Activate.ps1
```

#### Recreating the Virtual Environment

If you need to recreate your virtual environment (e.g., after upgrading Python, fixing package conflicts, or cleaning up after experiments):

```powershell
# Deactivate the current environment (if active)
deactivate

# Remove the existing virtual environment directory
Remove-Item -Recurse -Force .venv

# Create a fresh virtual environment
python -m venv .venv

# Activate the new environment
.\.venv\Scripts\Activate.ps1

# Reinstall all dependencies
pip install -r requirements.txt
```

**Note:** The convenience scripts `_venv.bat` and `_venv.ps1` in the project root can be used to quickly activate the virtual environment.

### 4. Install Requirements

Install dependencies from the provided requirements.txt:

```powershell
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the `devagents` directory to set up configuration as instructed in the `README` file.

### 6. Run DevAgents

Activate your virtual environment if not already active, then run:

```powershell
python -m cli.devagents --workflow <workflowName> --prompt "<prompt>" --workspace <workspace>
```

---

## 📦 Package Management

### Updating Microsoft Agent Framework

To update the Microsoft Agent Framework to the latest version:

```powershell
pip install --upgrade agent-framework[azure]
```

### Checking Current Version

To see which version of Microsoft Agent Framework is installed:

```powershell
pip show agent-framework
```

### Verifying Package Compatibility

After updating Microsoft Agent Framework or any other package, always check for dependency conflicts:

```powershell
pip check
```

If conflicts are reported, resolve them by:
1. Reinstalling the conflicting package to match requirements.txt:
   ```powershell
   pip install --force-reinstall <package>==<version>
   ```
2. Or updating requirements.txt with compatible versions

### Updating requirements.txt

After updating packages, you can regenerate requirements.txt:

```powershell
pip freeze > requirements.txt
```

**Important:** `pip freeze` will expand `agent-framework[azure]` into multiple individual packages. For maintainability, consider keeping only the main package in requirements.txt, for example:
```
agent-framework[azure]==1.0.0rc2
```

---

## 🧪 Running Tests

DevAgents uses pytest for testing. Tests are located in the `tests/` folder.

### Running All Tests

To run the complete test suite:

```powershell
# Using the test runner script
python tests/run_tests.py

# Or directly with pytest
pytest -s tests/
```

The `-s` flag shows print statements and console output during test execution.

### Running a Specific Test File

To run tests from a single file:

```powershell
pytest -s tests/test_research_agent.py
```

### Running a Single Test

To run just one specific test within a file:

```powershell
pytest -s tests/test_research_agent.py::test_research_basic_question__should_return_summary
```

### Common Pytest Options

- `-s` - Show console output (print statements)
- `-v` - Verbose mode (show individual test names)
- `-x` - Stop after first failure
- `-k <pattern>` - Run tests matching pattern (e.g., `-k "research"`)
- `--lf` - Run only tests that failed in the last run
- `--maxfail=<n>` - Stop after n failures

Example with multiple options:

```powershell
pytest -s -v -x tests/test_research_agent.py
```

---

## 🌦️ Testing Resources

### OpenWeatherMap

OpenWeatherMap is used in tests.  
- [OpenWeatherMap Sign In](https://home.openweathermap.org/users/sign_in)
- **Test Account:** `TEST_devagents_2025`

---

## 💡 Best Practices

- **Pin versions:** Always specify exact versions in requirements.txt for reproducibility
- **Check compatibility:** Run `pip check` after any package update
- **Test after updates:** Run the test suite to ensure nothing broke:
  ```powershell
  python tests/run_tests.py
  ```

---

## 🔧 Troubleshooting

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

> 💬 **Need more help?**  
> Reach out to the DevAgents team or check the project documentation for assistance.

Happy developing with DevAgents! 🚀

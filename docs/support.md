# 💡 DevAgents Support Instructions

Welcome to the **DevAgents** support guide!  
Below you'll find helpful tips and commands for maintaining and updating your development environment.

---

## 🚀 Microsoft Agent Framework (MAF) Package Management

### Updating MAF

To update the Microsoft Agent Framework to the latest version:

```powershell
pip install --upgrade agent-framework[azure]
```

### Checking Current Version

To see which version of MAF is installed:

```powershell
pip show agent-framework
```

### Verifying Package Compatibility

After updating MAF or any other package, always check for dependency conflicts:

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

**Important:** `pip freeze` will expand `agent-framework[azure]` into multiple individual packages. For maintainability, consider keeping only the main package in requirements.txt:
```
agent-framework[azure]==1.0.0b260127
```

---

## 📦 Best Practices

- **Pin versions:** Always specify exact versions in requirements.txt for reproducibility
- **Check compatibility:** Run `pip check` after any package update
- **Test after updates:** Run the test suite to ensure nothing broke:
  ```powershell
  python tests/run_tests.py
  ```

---

## 🌦️ OpenWeatherMap for Testing

OpenWeatherMap is used in tests.  
- [OpenWeatherMap Sign In](https://home.openweathermap.org/users/sign_in)
- **Test Account:** `TEST_devagents_2025`

---

> 💬 **Need more help?**  
> Reach out to the DevAgents team or check the project documentation for assistance.

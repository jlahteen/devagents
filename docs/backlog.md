# 🚀 DevAgents Backlog

Welcome to the **DevAgents** project backlog!  
Track ongoing progress, upcoming features, and known issues below.

---

## ⏳ Todo:
- hide .devagents directory?
- google search optional
- developer agent may not write all code in one message, reviewer should review
- when console closes, the status line is in the listing (as the first row)

## ✅ Done:
+ replace over_to in orchestrator agents
+ add errors to orchestrator_base and add errors
+ move devagents.py to cli
+ move all root level files to sub dirs
+ scenario engine layer added
+ monitoring added
+ fix tests

## 🟢 Current Iteration

- 🔄 **Change:** All arguments can be passed as command line arguments; missing arguments will be prompted
- 🔄 **Change:** Conversation between agents is now streamed to both the console and a trace file
- 🐞 **Bug:** Scaffold Agent is not always running commands with no user input
- 🔄 **Change:** `run_command` now shows lines without LF/CR (e.g., "Ok to proceed ?")
- 🔄 **Change:** Refactor BuildAgent to use an inner team
- 🔄 **Change:** Updated to AutoGen 0.5.7
- ✨ **New:** Support for Docker image releases added
- ✨ **New:** Linux support added

---

## 📋 Backlog

- 🐞 **Bug:** In case of an early AutoGen error, the monitor is not closed (e.g. "model_info is required when model name is not a valid OpenAI model")
- ✨ **New:** Add Java SDK to the container image, plus simple tests
- ✨ **New:** Add support for GO
- ✨ **New:** Add support for Rust
- ✨ **New:** Publish the Docker image to GitHub Container Registry
- ✨ **New:** Implement a generic base orchestrator for serving most scenarios
- 🐞 **Bug:** Add FixBug scenario
- ✨ **New:** Add NewSolution scenario
- ✨ **New:** Add NewFeature scenario
- 🔄 **Change:** Add ChangeFeature scenario
- ✨ **New:** Add NewComponent scenario
- 🔄 **Change:** Refactor google_search as intelligent (pass a free question as a param)
- 🐞 **Bug:** If a prompt file is not found, DevAgents starts to hallucinate
- 🐞 **Bug:** Add FixBuildWarnings scenario

---

> 💡 **Tip:**
> Have an idea or found a bug? Open an issue or contribute!

---
Happy prompting with DevAgents! 🚀

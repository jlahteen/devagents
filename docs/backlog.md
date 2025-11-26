# 🚀 DevAgents Backlog

Welcome to the **DevAgents** project backlog!  
Track ongoing progress, upcoming features, and known issues below.

---

## ⏳ Todo:
- 


## ✅ Done:
- 


## 🟢 Current Iteration

- ✨ **New:** ModifyCode scenario added
- ✨ **New:** ModifyApp scenario added
- ✨ **New:** New monitoring with a status line at the bottom of the console added
- 🔄 **Change:** All arguments can be passed as command line arguments; missing arguments will be prompted
- 🐞 **Bug:** Scaffold Agent was sometimes running commands requiring user input
- 🔄 **Change:** BuildAgent refactored to use an inner team
- 🔄 **Change:** Updated to AutoGen 0.5.7
- 🔄 **Change:** Google Search tool made optional
- ✨ **New:** Support for Docker image releases added
- ✨ **New:** Linux support added
- 🔄 **Change:** Internal architecture changes (e.g. scenario engine layer, CLI layer)

---

## 📋 Backlog

- 🐞 **Bug:** When console closes, the status line is in the listing (as the first row)
- 🐞 **Bug:** In case of an early AutoGen error, the monitor is not closed (e.g. "model_info is required when model name is not a valid OpenAI model")
- ✨ **New:** Add Java SDK to the container image, plus simple tests
- ✨ **New:** Add support for GO
- ✨ **New:** Add support for Rust
- ✨ **New:** Publish the Docker image to GitHub Container Registry
- 🐞 **Bug:** Add FixBug scenario
- ✨ **New:** Add NewSolution scenario
- ✨ **New:** Add NewFeature scenario
- 🔄 **Change:** Refactor google_search as intelligent (pass a free question as a param)
- 🐞 **Bug:** If a prompt file is not found, DevAgents starts to hallucinate

---

> 💡 **Tip:**
> Have an idea or found a bug? Open an issue or contribute!

---
Happy prompting with DevAgents! 🚀

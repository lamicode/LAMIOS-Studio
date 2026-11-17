# AGENTS.md — AI Development Partner Instructions (Gemini Website Edition)

This file governs all AI-assisted development for **LAMIOS Studio**.

## 1. Core Role & Philosophy
* Act as a coordinated 18-role engineering team (Principal Software Architect, Senior Python Developer, AI/ML Engineer, DSP Engineer, MIR Specialist, QA Engineer, and Beginner-Friendly Instructor).
* **Primary AI Interface:** `https://gemini.google.com`. Never instruct the user to install IDE coding extensions (Copilot, Cursor, Claude Code, Gemini Code Assist).
* **Local Tools:** Visual Studio Code is used strictly for local inspection, terminal commands, and running tests. GitHub Desktop is used for all version-control operations.
* **Beginner-Friendly Guidance:** Provide explicit step-by-step instructions for every Windows file operation, VS Code menu action, PowerShell command, and GitHub Desktop checkpoint. Always specify the working directory and distinguish PowerShell commands from Python code.

## 2. Capability Honesty Rules
* Never claim to have modified the user's local Windows files or pushed to GitHub.
* Treat GitHub imports or uploaded ZIPs as static snapshots.
* Clearly distinguish between remote syntax/unit validation and local Windows 11 hardware verification.
* Deliver updates as downloadable `.zip` packages accompanied by `CHANGE_MANIFEST.md`.

## 3. Hardware Constraints (Mandatory Safeguards)
The primary development machine runs an **Intel Core i7-1165G7 (4 cores), 15.8 GB RAM, and Intel Iris Xe Graphics (no NVIDIA CUDA)**:
1. **CPU-First Execution:** Every AI adapter must work reliably on CPU (`torch.device("cpu")` / `onnxruntime` CPUExecutionProvider) with optional GPU acceleration only when detected.
2. **Strict Memory Lifecycle:** Unload heavy models immediately after stage completion (`del model`, `gc.collect()`) so RAM usage stays well below the 15.8 GB ceiling.
3. **Chunked Processing:** Process full songs in overlapping windowed chunks backed by 32-bit float disk caches rather than holding multiple full-song tensors in RAM simultaneously.
4. **Non-Blocking UI:** Never run DSP or AI inference on the PySide6 GUI main thread.

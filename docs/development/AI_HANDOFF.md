# LAMIOS Studio — AI Handoff & Context Continuity Document

If starting a new conversation on `https://gemini.google.com`, upload this file along with `docs/development/PROJECT_STATUS.md` so Gemini immediately resumes with exact project context.

## 1. User & Workflow Context
* **Developer Experience Level:** Beginner-friendly step-by-step guidance required for all terminal commands, VS Code menus, file operations, and GitHub Desktop actions.
* **AI Interface:** Gemini Website (`gemini.google.com`) only. No IDE AI extensions.
* **Delivery Format:** Downloadable `.zip` packages containing complete files (never partial snippets) and `CHANGE_MANIFEST.md`, paired with the Section 39 Beginner Tutorial Format (Sections A through O) and Section 41 Development Report.

## 2. Locked Local Machine Specifications
* **OS:** Microsoft Windows 11 Pro 64-bit (10.0.26300)
* **CPU:** 11th Gen Intel(R) Core(TM) i7-1165G7 @ 2.80GHz (4 Cores, 4 Logical Processors)
* **RAM:** 15.8 GB
* **GPU:** Intel(R) Iris(R) Xe Graphics (1 GB integrated — **No NVIDIA CUDA**)
* **Authoritative Python:** Python 3.10.11 at `C:\Program Files\Python310\python.exe` (invoked via `py -3.10`)
* **Target Repository Path:** `C:\Users\lamio\Documents\GitHub\LAMIOS-Studio` (distinct from legacy `Lamios-Audio-Studio` project)

## 3. Licensing Policy Decision
* **Development & Internal Use Mode:** Modular adapter architecture. During development and personal use, any open-source library or model (including GPLv3 tools like `pedalboard` or research checkpoints) may be used behind clean adapter interfaces (`src/lamios/`), while tracking license metadata in `docs/models/MODEL_REGISTRY.md` so any component can be swapped if commercial redistribution is pursued later.

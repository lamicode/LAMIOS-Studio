# LAMIOS Studio

**AI-Powered Music Reconstruction, Audio Source Separation, Automatic Music Transcription, Virtual Instrumentation, Audio Restoration, and Digital Audio Workstation (DAW)**

* **Version:** 0.1.0 (Phase 0 — Architecture & Documentation Baseline)
* **Target Platform:** Microsoft Windows 11 (64-bit)
* **Primary Language:** Python 3.10.11 (64-bit)
* **GUI Framework:** PySide6 (Qt6)
* **Development Workflow:** Gemini Website Edition (`gemini.google.com`) + Visual Studio Code + GitHub Desktop

---

## 1. Overview

**LAMIOS Studio** accepts an existing full-mix song or live musical performance, identifies individual instruments and singers, separates them into independent audio stems where technically feasible, transcribes their performances into sample-accurate musical events, and constructs an editable multitrack project.

### Core Processing Pipeline
`Original Song` → `Source Detection` → `Hierarchical Instrument & Vocal Separation` → `Specialized Automatic Music Transcription & Note Fusion` → `Editable Multitrack Project` → `Sound Redesign & Virtual Instruments` → `Audio Restoration & Mixing` → `Audio / Stem / Optional MIDI Export`

### Three Synchronized Representations
1. **Original Audio:** Immutable, lossless working reference anchored to original sample positions.
2. **Separated Audio:** Broad stems, fine sub-stems, drum sub-components, and preserved residual signals with confidence scores.
3. **Musical Performance Data:** Structured internal note events, drum hits, continuous vocal pitch/vibrato curves, expression, and music theory grids (independent of MIDI export).

---

## 2. Verified Development Hardware & Environment Baseline

Locked during **Phase 0, Task 0.1**:
* **OS:** Microsoft Windows 11 Pro 64-bit (Build 10.0.26300)
* **CPU:** 11th Gen Intel Core i7-1165G7 @ 2.80 GHz (4 Cores / 4 Logical Processors)
* **System RAM:** 15.8 GB (~16 GB)
* **Graphics:** Intel Iris Xe Graphics (Integrated — CPU-Safe execution mode is mandatory default; no NVIDIA CUDA dependency)
* **Authoritative Python Interpreter:** Python 3.10.11 (`C:\Program Files\Python310\python.exe` via `py -3.10`)
* **Editor & Version Control:** Visual Studio Code 1.146.0 (x64) + GitHub Desktop (`git 2.52.0.windows.1`)

---

## 3. Repository Structure

```text
LAMIOS-Studio/
├── README.md
├── AGENTS.md
├── CHANGE_MANIFEST.md
├── .gitignore
├── .env.example
└── docs/
    ├── MASTER_BLUEPRINT.md
    ├── architecture/
    │   └── SYSTEM_ARCHITECTURE.md
    ├── development/
    │   ├── DEVELOPMENT_PLAN.md
    │   ├── PROJECT_STATUS.md
    │   ├── AI_HANDOFF.md
    │   ├── KNOWN_ISSUES.md
    │   └── CHANGELOG.md
    ├── models/
    │   └── MODEL_REGISTRY.md
    └── testing/
        └── TEST_RESULTS.md
```
*(Source packages under `src/lamios/` and `tests/` are created incrementally starting in Phase 1.)*

---

## 4. Documentation Index

* [`AGENTS.md`](AGENTS.md) — Mandatory rules for the AI development partner.
* [`docs/MASTER_BLUEPRINT.md`](docs/MASTER_BLUEPRINT.md) — Unified Master Software Development Blueprint (v3.0).
* [`docs/architecture/SYSTEM_ARCHITECTURE.md`](docs/architecture/SYSTEM_ARCHITECTURE.md) — Layered architecture, data contracts, sample timeline rules, and `.lamios` schema.
* [`docs/development/DEVELOPMENT_PLAN.md`](docs/development/DEVELOPMENT_PLAN.md) — Phased implementation roadmap (Phases 0–19).
* [`docs/development/PROJECT_STATUS.md`](docs/development/PROJECT_STATUS.md) — Live milestone tracker.
* [`docs/development/AI_HANDOFF.md`](docs/development/AI_HANDOFF.md) — Session continuity reference for new Gemini chats.
* [`docs/models/MODEL_REGISTRY.md`](docs/models/MODEL_REGISTRY.md) — Candidate AI models, resource budgets, and licensing audit.

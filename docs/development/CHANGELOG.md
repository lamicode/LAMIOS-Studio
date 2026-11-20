# Changelog

All notable changes to **LAMIOS Studio** are documented in this file.

## [0.1.1-phase1.1] - 2026-11-21
### Added
- Added `pyproject.toml` configured for Python 3.10 (`>=3.10,<3.12`), `PySide6`, `numpy`, `psutil`, and dev QA tools (`pytest`, `pytest-qt`, `pytest-cov`, `ruff`, `mypy`).
- Implemented `src/lamios/__init__.py` and `src/lamios/core/` foundation package:
  - `config.py`: CPU-safe `.env` and environment variable configuration loader.
  - `logging_setup.py`: Structured rotating file + console logging subsystem.
  - `hardware.py`: Non-blocking `psutil` CPU/RAM/CUDA hardware telemetry monitor.
  - `models.py`: Versioned sample-accurate data contracts (`AudioAssetRef`, `StemArtifact`, `NoteEvent`, `DrumEvent`, `TrackMetadata`).
- Added automated unit test suite (`tests/unit/test_core_foundation.py`) covering all core foundation modules.

## [0.1.0-phase0] - 2026-11-18
### Added
- Completed Phase 0, Task 0.1 Windows 11 hardware, Python 3.10.11, VS Code, and GitHub Desktop audit.
- Initialized repository scaffolding (`.gitignore`, `.env.example`, `README.md`, `AGENTS.md`).
- Added authoritative `docs/MASTER_BLUEPRINT.md` (Version 3.0), `SYSTEM_ARCHITECTURE.md`, `MODEL_REGISTRY.md`, and development tracking documents.

# Changelog

All notable changes to **LAMIOS Studio** are documented in this file.

## [0.1.2-phase1.2] - 2026-11-21
### Added
- Implemented `src/lamios/gui/theme.py` providing default Dark Mode and optional Light Mode QSS workstation themes.
- Implemented `src/lamios/gui/panels.py` with `ProjectDashboardPanel`, `ProcessingMonitorPanel`, and honest phase-labeled workspace panels.
- Implemented `src/lamios/gui/main_window.py` (`LamiosMainWindow`) featuring 5 central tabs (Dashboard, Arrangement, Piano Roll, Vocal Editor, Drum Editor), 5 dockable DAW panels, transport toolbar stub, View/Theme/Reset Layout menus, and live non-blocking CPU/RAM telemetry.
- Added application entry points `src/lamios/app/main.py`, `src/lamios/__main__.py`, and `[project.scripts]` command `lamios-studio` in `pyproject.toml`.
- Added 4 automated `pytest-qt` GUI tests in `tests/gui/test_main_window.py`.

## [0.1.1-phase1.1] - 2026-11-21
### Added
- Added `pyproject.toml` configured for Python 3.10 (`>=3.10,<3.12`), `PySide6`, `numpy`, `psutil`, and dev QA tools.
- Implemented `src/lamios/core/` (`config.py`, `logging_setup.py`, `hardware.py`, `models.py`) and 8 unit tests in `tests/unit/test_core_foundation.py`.
- Verified locally on Windows 11 (8/8 `pytest` passed, `ruff check src tests` passed).

## [0.1.0-phase0] - 2026-11-18
### Added
- Completed Phase 0 Windows 11 hardware/Python 3.10.11 audit and initialized authoritative repository documentation and schemas.

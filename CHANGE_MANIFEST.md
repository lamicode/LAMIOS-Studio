# CHANGE MANIFEST — LAMIOS Studio

1. **Package Identifier:** `LAMIOS-Phase-01-Task-01-Foundation`
2. **Development Phase:** Phase 1 — Environment and Application Foundation (Task 1.1)
3. **Expected Base Revision:** Phase 0 initial commit on `main` (`Phase 0: Initialize LAMIOS Studio blueprint, architecture, and model registry`)
4. **New Files (10 files):**
   - `pyproject.toml`
   - `src/lamios/__init__.py`
   - `src/lamios/core/__init__.py`
   - `src/lamios/core/config.py`
   - `src/lamios/core/logging_setup.py`
   - `src/lamios/core/hardware.py`
   - `src/lamios/core/models.py`
   - `tests/__init__.py`
   - `tests/unit/__init__.py`
   - `tests/unit/test_core_foundation.py`
5. **Modified Files (3 files):**
   - `CHANGE_MANIFEST.md`
   - `docs/development/PROJECT_STATUS.md`
   - `docs/development/CHANGELOG.md`
6. **Proposed Deletions:** None
7. **New Dependencies:**
   - Runtime: `PySide6>=6.6.0,<6.9.0`, `numpy>=1.24.0,<2.0.0`, `psutil>=5.9.0`
   - Development/QA: `pytest>=8.0.0`, `pytest-qt>=4.4.0`, `pytest-cov>=5.0.0`, `ruff>=0.4.0`, `mypy>=1.10.0`
8. **Configuration Changes:** Added `pyproject.toml` configuring editable src-layout packaging, `pytest`, `ruff`, and `mypy`.
9. **Installation Steps:**
   - Create feature branch `phase-01-foundation` in GitHub Desktop.
   - Extract ZIP to a temporary Downloads folder and copy contents into `C:\Users\lamio\Documents\GitHub\LAMIOS-Studio\`, replacing the 3 updated docs/manifest files.
   - Create `.venv` with `py -3.10 -m venv .venv`, activate it, and run `pip install -e ".[dev]"`.
10. **Tests Executed (Remote — Python 3.10 Sandbox):**
    - `py_compile` syntax validation across all 9 Python files (PASSED).
    - Direct Python 3.10 execution of all 8 core foundation logic scenarios against `lamios.core` (`config`, `logging_setup`, `models`, and `hardware` with mocked `psutil`) (PASSED).
    - `zipfile.testzip()` archive integrity check (PASSED).
11. **Tests Not Executed (Remote):** `pytest` CLI runner, real `psutil` hardware polling, `PySide6` installation, and `ruff` / `mypy` execution on Windows 11 (requires your local Python 3.10.11 `.venv`).
12. **Known Issues:** PySide6 GUI window is intentionally scheduled for Task 1.2 so Task 1.1 cleanly verifies the Python 3.10 environment and core data layer first.
13. **Rollback Instructions:** In GitHub Desktop, discard changes on branch `phase-01-foundation` or switch back to `main`.
14. **Acceptance Criteria:**
    - `.venv` created using Python 3.10.11 inside `C:\Users\lamio\Documents\GitHub\LAMIOS-Studio\.venv`.
    - `pip install -e ".[dev]"` completes without errors.
    - `pytest -v` passes all 8 unit tests on your Windows 11 PC.
    - `ruff check src tests` reports zero errors.
    - Changes committed and pushed on branch `phase-01-foundation` in GitHub Desktop.

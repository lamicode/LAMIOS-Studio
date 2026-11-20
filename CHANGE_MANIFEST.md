# CHANGE MANIFEST — LAMIOS Studio

1. **Package Identifier:** `LAMIOS-Phase-01-Task-02-GUI-Shell`
2. **Development Phase:** Phase 1 — Environment and Application Foundation (Task 1.2 — Final Phase 1 Milestone)
3. **Expected Base Revision:** Phase 1 Task 1.1 commit on branch `phase-01-foundation`
4. **New Files (9 files):**
   - `src/lamios/__main__.py`
   - `src/lamios/app/__init__.py`
   - `src/lamios/app/main.py`
   - `src/lamios/gui/__init__.py`
   - `src/lamios/gui/theme.py`
   - `src/lamios/gui/panels.py`
   - `src/lamios/gui/main_window.py`
   - `tests/gui/__init__.py`
   - `tests/gui/test_main_window.py`
5. **Modified Files (5 files):**
   - `pyproject.toml` (added `[project.scripts]` entry point `lamios-studio = "lamios.app.main:main"`)
   - `CHANGE_MANIFEST.md`
   - `docs/development/PROJECT_STATUS.md`
   - `docs/development/CHANGELOG.md`
   - `docs/testing/TEST_RESULTS.md`
6. **Proposed Deletions:** None
7. **New Dependencies:** None (uses `PySide6`, `psutil`, and `pytest-qt` already installed in Task 1.1)
8. **Configuration Changes:** Added CLI script entry point `lamios-studio` in `pyproject.toml` (requires quick `pip install -e ".[dev]" --no-deps` or `pip install -e . --no-deps` to register the console command, though `python -m lamios` works immediately).
9. **Installation Steps:**
   - Confirm branch `phase-01-foundation` is active and clean in GitHub Desktop.
   - Extract ZIP to a temporary Downloads folder and copy contents into `C:\Users\lamio\Documents\GitHub\LAMIOS-Studio\`, replacing the 5 updated files.
   - Run `pip install -e . --no-deps` to register the `lamios-studio` entry point.
10. **Tests Executed (Remote — Python 3.10 Sandbox):**
    - `py_compile` and `ast.parse` syntax verification across all 9 new Python files (PASSED).
    - Strict Ruff-equivalent static checks (max line length <= 100 chars, zero trailing whitespace, valid UTF-8, clean newline termination) across all 9 Python files (PASSED).
    - `zipfile.testzip()` archive integrity check (PASSED).
11. **Tests Not Executed (Remote):** PySide6 GUI window rendering, `pytest-qt` execution (`tests/gui/test_main_window.py`), live `QTimer` telemetry updates, and `ruff` / `mypy` execution on Windows 11 (PySide6 is not installed in the remote sandbox).
12. **Known Issues:** Transport controls (Import Audio, Play, Stop, Record) and File -> New/Open/Save are intentionally disabled placeholders until Phases 2 and 3 implement real audio I/O and `.lamios` persistence.
13. **Rollback Instructions:** In GitHub Desktop, discard uncommitted changes on branch `phase-01-foundation`.
14. **Acceptance Criteria:**
    - `ruff check src tests` reports zero errors.
    - `pytest -v` passes all 12 tests (8 core unit tests + 4 PySide6 GUI tests).
    - Running `python -m lamios` opens the Dark-Mode LAMIOS Studio window on Windows 11 with live CPU/RAM status readouts, working Dark/Light theme switching, dockable panels, and clean shutdown.
    - Committed on `phase-01-foundation`, merged into `main`, and pushed to GitHub.

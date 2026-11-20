"""Automated pytest-qt GUI tests for the LAMIOS Studio workstation shell."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QApplication
from pytestqt.qtbot import QtBot

from lamios import __app_name__, __version__
from lamios.core import HardwareMonitor, load_config
from lamios.gui import LamiosMainWindow, get_stylesheet


def test_main_window_launches_with_expected_workspace_and_docks(
    qtbot: QtBot, tmp_path: Path
) -> None:
    cfg = load_config(project_root=tmp_path)
    window = LamiosMainWindow(config=cfg, hardware_monitor=HardwareMonitor())
    qtbot.addWidget(window)
    window.show()

    assert window.windowTitle() == f"{__app_name__} v{__version__}"
    assert window.central_tabs.count() == 5
    tab_titles = [window.central_tabs.tabText(i) for i in range(window.central_tabs.count())]
    assert tab_titles == [
        "Dashboard",
        "Arrangement",
        "Piano Roll",
        "Vocal Editor",
        "Drum Editor",
    ]
    assert set(window.docks.keys()) == {
        "import_ai",
        "browser",
        "mixer",
        "monitor",
        "models_export",
    }
    assert "CPU:" in window.cpu_badge.text()
    assert "RAM:" in window.ram_badge.text()


def test_theme_switching_updates_state_and_stylesheet(qtbot: QtBot, tmp_path: Path) -> None:
    cfg = load_config(project_root=tmp_path)
    window = LamiosMainWindow(config=cfg, hardware_monitor=HardwareMonitor())
    qtbot.addWidget(window)

    assert window.current_theme == "dark"
    assert window.action_theme_dark.isChecked()
    assert not window.action_theme_light.isChecked()

    window.set_theme("light")
    assert window.current_theme == "light"
    assert window.action_theme_light.isChecked()
    app = QApplication.instance()
    assert isinstance(app, QApplication)
    assert app.styleSheet() == get_stylesheet("light")

    window.set_theme("dark")
    assert window.current_theme == "dark"
    assert app.styleSheet() == get_stylesheet("dark")


def test_dock_visibility_and_reset_layout(qtbot: QtBot, tmp_path: Path) -> None:
    cfg = load_config(project_root=tmp_path)
    window = LamiosMainWindow(config=cfg, hardware_monitor=HardwareMonitor())
    qtbot.addWidget(window)
    window.show()

    models_dock = window.docks["models_export"]
    models_dock.hide()
    assert not models_dock.isVisible()

    window.reset_layout()
    assert models_dock.isVisible()


def test_hardware_telemetry_refresh_and_clean_close(qtbot: QtBot, tmp_path: Path) -> None:
    cfg = load_config(project_root=tmp_path)
    window = LamiosMainWindow(config=cfg, hardware_monitor=HardwareMonitor())
    qtbot.addWidget(window)

    snapshot = window.refresh_hardware_telemetry()
    assert snapshot.ram_total_gb > 0.0
    assert f"{snapshot.ram_total_gb:.1f}" in window.ram_badge.text()
    assert window.telemetry_timer.isActive()

    window.close()
    assert not window.telemetry_timer.isActive()

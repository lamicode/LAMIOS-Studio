"""Dark and Light workstation QSS stylesheets for LAMIOS Studio."""

from __future__ import annotations

from typing import Literal

from PySide6.QtWidgets import QApplication

ThemeName = Literal["dark", "light"]

DARK_STYLESHEET = """
QMainWindow, QWidget {
    background-color: #14171D;
    color: #E5E7EB;
    font-family: "Segoe UI", "Inter", sans-serif;
    font-size: 9.5pt;
}

QMenuBar {
    background-color: #101318;
    color: #E5E7EB;
    border-bottom: 1px solid #262C38;
    padding: 2px 4px;
}

QMenuBar::item:selected {
    background-color: #252D3D;
    border-radius: 4px;
}

QMenu {
    background-color: #1A1F29;
    color: #E5E7EB;
    border: 1px solid #2E3646;
    padding: 4px;
}

QMenu::item:selected {
    background-color: #2563EB;
    color: #FFFFFF;
    border-radius: 3px;
}

QToolBar {
    background-color: #181C24;
    border-bottom: 1px solid #262C38;
    spacing: 6px;
    padding: 4px 8px;
}

QToolButton, QPushButton {
    background-color: #232A36;
    color: #E5E7EB;
    border: 1px solid #333C4D;
    border-radius: 4px;
    padding: 5px 10px;
}

QToolButton:hover, QPushButton:hover {
    background-color: #2D3646;
    border-color: #3B82F6;
}

QToolButton:disabled, QPushButton:disabled {
    background-color: #1B202A;
    color: #6B7280;
    border-color: #262C38;
}

QDockWidget {
    color: #D1D5DB;
    titlebar-close-icon: none;
}

QDockWidget::title {
    background-color: #1B202B;
    border: 1px solid #262C38;
    padding: 5px 8px;
    font-weight: 600;
}

QTabWidget::pane {
    border: 1px solid #262C38;
    background-color: #181C24;
}

QTabBar::tab {
    background-color: #14171D;
    color: #9CA3AF;
    border: 1px solid #262C38;
    border-bottom: none;
    padding: 6px 14px;
    margin-right: 2px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}

QTabBar::tab:selected {
    background-color: #1F2633;
    color: #FFFFFF;
    border-top: 2px solid #3B82F6;
}

QFrame#WorkspaceCard {
    background-color: #1B202B;
    border: 1px solid #2B3344;
    border-radius: 8px;
}

QLabel#TitleLabel {
    font-size: 14pt;
    font-weight: 700;
    color: #F9FAFB;
}

QLabel#SubtitleLabel {
    font-size: 9.5pt;
    color: #9CA3AF;
}

QLabel#BadgeLabel {
    background-color: #1E3A5F;
    color: #93C5FD;
    border: 1px solid #2563EB;
    border-radius: 10px;
    padding: 2px 10px;
    font-size: 8.5pt;
    font-weight: 600;
}

QLabel#MonoReadout {
    background-color: #0F1217;
    color: #38BDF8;
    border: 1px solid #262C38;
    border-radius: 4px;
    padding: 4px 10px;
    font-family: "Consolas", "Cascadia Mono", monospace;
    font-size: 10.5pt;
    font-weight: 600;
}

QStatusBar {
    background-color: #101318;
    color: #9CA3AF;
    border-top: 1px solid #262C38;
}

QStatusBar::item {
    border: none;
}

QLabel#TelemetryBadge {
    color: #D1D5DB;
    padding: 1px 8px;
    font-family: "Consolas", monospace;
    font-size: 8.5pt;
}

QLabel#TelemetryWarning {
    background-color: #7F1D1D;
    color: #FECACA;
    border-radius: 3px;
    padding: 1px 8px;
    font-family: "Consolas", monospace;
    font-size: 8.5pt;
    font-weight: 600;
}
"""

LIGHT_STYLESHEET = """
QMainWindow, QWidget {
    background-color: #F3F4F6;
    color: #111827;
    font-family: "Segoe UI", "Inter", sans-serif;
    font-size: 9.5pt;
}

QMenuBar {
    background-color: #FFFFFF;
    color: #111827;
    border-bottom: 1px solid #D1D5DB;
    padding: 2px 4px;
}

QMenuBar::item:selected {
    background-color: #E5E7EB;
    border-radius: 4px;
}

QMenu {
    background-color: #FFFFFF;
    color: #111827;
    border: 1px solid #D1D5DB;
    padding: 4px;
}

QMenu::item:selected {
    background-color: #2563EB;
    color: #FFFFFF;
    border-radius: 3px;
}

QToolBar {
    background-color: #F9FAFB;
    border-bottom: 1px solid #D1D5DB;
    spacing: 6px;
    padding: 4px 8px;
}

QToolButton, QPushButton {
    background-color: #FFFFFF;
    color: #111827;
    border: 1px solid #D1D5DB;
    border-radius: 4px;
    padding: 5px 10px;
}

QToolButton:hover, QPushButton:hover {
    background-color: #EFF6FF;
    border-color: #2563EB;
}

QToolButton:disabled, QPushButton:disabled {
    background-color: #F3F4F6;
    color: #9CA3AF;
}

QDockWidget::title {
    background-color: #E5E7EB;
    border: 1px solid #D1D5DB;
    padding: 5px 8px;
    font-weight: 600;
}

QTabWidget::pane {
    border: 1px solid #D1D5DB;
    background-color: #FFFFFF;
}

QTabBar::tab {
    background-color: #E5E7EB;
    color: #4B5563;
    border: 1px solid #D1D5DB;
    border-bottom: none;
    padding: 6px 14px;
    margin-right: 2px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}

QTabBar::tab:selected {
    background-color: #FFFFFF;
    color: #111827;
    border-top: 2px solid #2563EB;
}

QFrame#WorkspaceCard {
    background-color: #FFFFFF;
    border: 1px solid #D1D5DB;
    border-radius: 8px;
}

QLabel#TitleLabel {
    font-size: 14pt;
    font-weight: 700;
    color: #111827;
}

QLabel#SubtitleLabel {
    font-size: 9.5pt;
    color: #4B5563;
}

QLabel#BadgeLabel {
    background-color: #DBEAFE;
    color: #1D4ED8;
    border: 1px solid #93C5FD;
    border-radius: 10px;
    padding: 2px 10px;
    font-size: 8.5pt;
    font-weight: 600;
}

QLabel#MonoReadout {
    background-color: #111827;
    color: #38BDF8;
    border: 1px solid #374151;
    border-radius: 4px;
    padding: 4px 10px;
    font-family: "Consolas", "Cascadia Mono", monospace;
    font-size: 10.5pt;
    font-weight: 600;
}

QStatusBar {
    background-color: #FFFFFF;
    color: #4B5563;
    border-top: 1px solid #D1D5DB;
}

QLabel#TelemetryBadge {
    color: #1F2937;
    padding: 1px 8px;
    font-family: "Consolas", monospace;
    font-size: 8.5pt;
}

QLabel#TelemetryWarning {
    background-color: #FEE2E2;
    color: #991B1B;
    border-radius: 3px;
    padding: 1px 8px;
    font-family: "Consolas", monospace;
    font-size: 8.5pt;
    font-weight: 600;
}
"""


def get_stylesheet(theme: ThemeName) -> str:
    """Return the QSS stylesheet for the requested theme ('dark' or 'light')."""
    if theme == "dark":
        return DARK_STYLESHEET
    if theme == "light":
        return LIGHT_STYLESHEET
    raise ValueError(f"Unsupported theme: {theme!r}")


def apply_theme(app: QApplication, theme: ThemeName) -> None:
    """Apply the specified workstation theme across the entire QApplication."""
    app.setStyleSheet(get_stylesheet(theme))

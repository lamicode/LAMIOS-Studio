"""Main desktop application bootstrap for LAMIOS Studio (PySide6)."""

from __future__ import annotations

import sys
from collections.abc import Sequence

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from lamios import __app_name__, __version__
from lamios.core import AppConfig, HardwareMonitor, configure_logging, get_logger, load_config
from lamios.gui import LamiosMainWindow, apply_theme


def create_application(argv: Sequence[str] | None = None) -> QApplication:
    """Create or reuse a QApplication configured for High-DPI Windows rendering."""
    existing = QApplication.instance()
    if isinstance(existing, QApplication):
        app = existing
    else:
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )
        app = QApplication(list(argv) if argv is not None else sys.argv)

    app.setApplicationName(__app_name__)
    app.setApplicationVersion(__version__)
    app.setOrganizationName("Lamios")
    apply_theme(app, "dark")
    return app


def main(argv: Sequence[str] | None = None, config: AppConfig | None = None) -> int:
    """Initialize configuration, logging, hardware telemetry, and launch the GUI."""
    cfg = config or load_config()
    cfg.ensure_runtime_directories()
    configure_logging(logs_dir=cfg.logs_dir, log_level=cfg.log_level)

    logger = get_logger("app.main")
    logger.info("Launching %s v%s (env=%s)", __app_name__, __version__, cfg.env)

    app = create_application(argv)
    monitor = HardwareMonitor(ram_warning_threshold_percent=cfg.max_ram_usage_percent)
    window = LamiosMainWindow(config=cfg, hardware_monitor=monitor)
    window.show()

    exit_code = app.exec()
    logger.info("%s exited cleanly (code=%d)", __app_name__, exit_code)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())

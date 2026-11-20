"""Main PySide6 dockable workstation window for LAMIOS Studio."""

from __future__ import annotations

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction, QActionGroup, QCloseEvent
from PySide6.QtWidgets import (
    QApplication,
    QDockWidget,
    QLabel,
    QMainWindow,
    QMessageBox,
    QStatusBar,
    QTabWidget,
    QToolBar,
    QWidget,
)

from lamios import __app_name__, __version__
from lamios.core import AppConfig, HardwareMonitor, HardwareSnapshot, get_logger, load_config
from lamios.gui.panels import PlaceholderPanel, ProcessingMonitorPanel, ProjectDashboardPanel
from lamios.gui.theme import ThemeName, apply_theme

logger = get_logger("gui.main_window")


class LamiosMainWindow(QMainWindow):
    """Primary workstation shell containing dockable DAW panels and live hardware telemetry."""

    def __init__(
        self,
        config: AppConfig | None = None,
        hardware_monitor: HardwareMonitor | None = None,
        telemetry_interval_ms: int = 2000,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.config = config or load_config()
        self.hardware_monitor = hardware_monitor or HardwareMonitor(
            ram_warning_threshold_percent=self.config.max_ram_usage_percent
        )
        self.current_theme: ThemeName = "dark"
        self.docks: dict[str, QDockWidget] = {}

        self.setWindowTitle(f"{__app_name__} v{__version__}")
        self.resize(1360, 840)
        self.setMinimumSize(1024, 640)
        self.setDockOptions(
            QMainWindow.DockOption.AllowNestedDocks
            | QMainWindow.DockOption.AllowTabbedDocks
            | QMainWindow.DockOption.AnimatedDocks
        )

        self._build_central_workspace()
        self._build_docks()
        self._build_toolbar()
        self._build_menus()
        self._build_status_bar()

        self._initial_dock_state = self.saveState()

        self.telemetry_timer = QTimer(self)
        self.telemetry_timer.setInterval(telemetry_interval_ms)
        self.telemetry_timer.timeout.connect(self.refresh_hardware_telemetry)
        self.refresh_hardware_telemetry()
        self.telemetry_timer.start()

        logger.info("LamiosMainWindow initialized successfully")

    def _build_central_workspace(self) -> None:
        self.central_tabs = QTabWidget(self)
        self.central_tabs.setDocumentMode(True)

        self.dashboard_panel = ProjectDashboardPanel(self.config, self)
        self.arrangement_panel = PlaceholderPanel(
            title="Multitrack Arrangement View",
            phase_label="Phases 2–3",
            description=(
                "Sample-accurate multitrack timeline displaying original recordings, "
                "broad/fine separated stems, unresolved group tracks, and waveforms."
            ),
            capabilities=[
                "Original immutable audio reference track + synchronized stem lanes",
                "Track color coding, mute/solo controls, and playback cursor seeking",
                "Non-destructive Undo/Redo editing backed by native .lamios projects",
            ],
            parent=self,
        )
        self.piano_roll_panel = PlaceholderPanel(
            title="Multitrack Piano-Roll Editor",
            phase_label="Phase 8",
            description=(
                "Hardware-accelerated Qt note editor displaying sample-accurate NoteEvents, "
                "velocity lanes, pitch-bend curves, and AI confidence indicators."
            ),
            capabilities=[
                "Individual instrument views and combined color-coded multitrack overlay",
                "Grid snapping, quantization, note creation/resizing, and chord labels",
                "Independent from MIDI (MIDI export remains strictly optional)",
            ],
            parent=self,
        )
        self.vocal_editor_panel = PlaceholderPanel(
            title="Vocal & Singer Editor",
            phase_label="Phase 10",
            description=(
                "Dedicated continuous pitch, vibrato, and singer-assignment editor for "
                "lead and backing vocals."
            ),
            capabilities=[
                "Continuous pitch-curve visualization and formant-aware editing",
                "Lead/backing vocal clustering and manual singer track reassignment",
                "Confidence-aware vocal transcription and optional lyric alignment",
            ],
            parent=self,
        )
        self.drum_editor_panel = PlaceholderPanel(
            title="Drum & Percussion Lane Editor",
            phase_label="Phase 9",
            description=(
                "Dedicated percussion lane workspace separating kick, snare, hi-hat, "
                "toms, and cymbals from pitched melodic tracks."
            ),
            capabilities=[
                "Transient hit lanes with per-hit velocity and timing offset controls",
                "Quantization, swing, and per-drum sample replacement",
                "Optional drum MIDI export without forcing melodic pitch representation",
            ],
            parent=self,
        )

        self.central_tabs.addTab(self.dashboard_panel, "Dashboard")
        self.central_tabs.addTab(self.arrangement_panel, "Arrangement")
        self.central_tabs.addTab(self.piano_roll_panel, "Piano Roll")
        self.central_tabs.addTab(self.vocal_editor_panel, "Vocal Editor")
        self.central_tabs.addTab(self.drum_editor_panel, "Drum Editor")
        self.setCentralWidget(self.central_tabs)

    def _create_dock(
        self,
        key: str,
        title: str,
        widget: QWidget,
        area: Qt.DockWidgetArea,
    ) -> QDockWidget:
        dock = QDockWidget(title, self)
        dock.setObjectName(f"Dock_{key}")
        dock.setWidget(widget)
        dock.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea
            | Qt.DockWidgetArea.RightDockWidgetArea
            | Qt.DockWidgetArea.BottomDockWidgetArea
        )
        self.addDockWidget(area, dock)
        self.docks[key] = dock
        return dock

    def _build_docks(self) -> None:
        import_ai_widget = PlaceholderPanel(
            title="Audio Import & AI Analysis",
            phase_label="Phases 2–7",
            description="Import full songs or live audio and run hierarchical AI analysis.",
            capabilities=[
                "WAV, FLAC, MP3, OGG, AIFF, M4A import + WASAPI live capture",
                "Chunked CPU-safe source separation with residual preservation",
                "Instrument detection, model routing, and confidence reporting",
            ],
            parent=self,
        )
        browser_widget = PlaceholderPanel(
            title="Instruments & Effects Browser",
            phase_label="Phases 12–14",
            description="Browse SoundFonts, virtual synths, restoration tools, and FX chains.",
            capabilities=[
                "Original stem, reconstructed virtual instrument, or blended playback",
                "Per-track EQ, compression, reverb, delay, and restoration presets",
            ],
            parent=self,
        )
        mixer_widget = PlaceholderPanel(
            title="Multitrack Mixer",
            phase_label="Phase 14",
            description="Channel faders, panning, metering, mute/solo, buses, and master output.",
            capabilities=[
                "Independent per-track effects chain and automation lanes",
                "Real-time peak/RMS metering isolated from AI worker threads",
            ],
            parent=self,
        )
        self.processing_monitor = ProcessingMonitorPanel(self)
        model_export_widget = PlaceholderPanel(
            title="Model Manager & Export Center",
            phase_label="Phases 5 & 16",
            description="Inspect AI model adapters, license metadata, and export targets.",
            capabilities=[
                "Versioned model registry with checksum & CPU/RAM compatibility",
                "Lossless WAV/FLAC stem export + optional Type 1 / per-track MIDI",
            ],
            parent=self,
        )

        dock_import = self._create_dock(
            "import_ai",
            "Import & AI Analysis",
            import_ai_widget,
            Qt.DockWidgetArea.LeftDockWidgetArea,
        )
        dock_browser = self._create_dock(
            "browser",
            "Instruments & FX",
            browser_widget,
            Qt.DockWidgetArea.LeftDockWidgetArea,
        )
        self.tabifyDockWidget(dock_import, dock_browser)
        dock_import.raise_()

        dock_mixer = self._create_dock(
            "mixer",
            "Mixer",
            mixer_widget,
            Qt.DockWidgetArea.BottomDockWidgetArea,
        )
        dock_monitor = self._create_dock(
            "monitor",
            "Processing Monitor",
            self.processing_monitor,
            Qt.DockWidgetArea.BottomDockWidgetArea,
        )
        self.tabifyDockWidget(dock_mixer, dock_monitor)
        dock_monitor.raise_()

        self._create_dock(
            "models_export",
            "Models & Export",
            model_export_widget,
            Qt.DockWidgetArea.RightDockWidgetArea,
        )

    def _build_toolbar(self) -> None:
        toolbar = QToolBar("Transport Toolbar", self)
        toolbar.setObjectName("TransportToolbar")
        toolbar.setMovable(False)

        self.action_import_audio = QAction("Import Audio", self)
        self.action_import_audio.setToolTip("Import audio file (Scheduled for Phase 2)")
        self.action_import_audio.setEnabled(False)

        self.action_play = QAction("Play", self)
        self.action_play.setToolTip("Play / Pause audio transport (Scheduled for Phase 2)")
        self.action_play.setEnabled(False)

        self.action_stop = QAction("Stop", self)
        self.action_stop.setToolTip("Stop transport and return to start (Scheduled for Phase 2)")
        self.action_stop.setEnabled(False)

        self.action_record = QAction("Record", self)
        self.action_record.setToolTip("Live WASAPI audio capture (Scheduled for Phase 2)")
        self.action_record.setEnabled(False)

        toolbar.addAction(self.action_import_audio)
        toolbar.addSeparator()
        toolbar.addAction(self.action_play)
        toolbar.addAction(self.action_stop)
        toolbar.addAction(self.action_record)
        toolbar.addSeparator()

        self.timeline_readout = QLabel("00:00:00.000  |  44.1 kHz  |  120.0 BPM", self)
        self.timeline_readout.setObjectName("MonoReadout")
        toolbar.addWidget(self.timeline_readout)

        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

    def _build_menus(self) -> None:
        menu_bar = self.menuBar()

        # File Menu
        file_menu = menu_bar.addMenu("&File")
        new_project_act = QAction("&New Project (Phase 3)", self)
        new_project_act.setEnabled(False)
        open_project_act = QAction("&Open .lamios Project... (Phase 3)", self)
        open_project_act.setEnabled(False)
        save_project_act = QAction("&Save Project (Phase 3)", self)
        save_project_act.setEnabled(False)
        exit_act = QAction("E&xit", self)
        exit_act.setShortcut("Ctrl+Q")
        exit_act.triggered.connect(self.close)

        file_menu.addAction(new_project_act)
        file_menu.addAction(open_project_act)
        file_menu.addAction(save_project_act)
        file_menu.addSeparator()
        file_menu.addAction(exit_act)

        # View Menu
        view_menu = menu_bar.addMenu("&View")
        panels_menu = view_menu.addMenu("&Panels")
        for dock in self.docks.values():
            panels_menu.addAction(dock.toggleViewAction())

        reset_layout_act = QAction("&Reset Workstation Layout", self)
        reset_layout_act.triggered.connect(self.reset_layout)
        view_menu.addAction(reset_layout_act)
        view_menu.addSeparator()

        theme_menu = view_menu.addMenu("&Theme")
        theme_group = QActionGroup(self)
        theme_group.setExclusive(True)

        self.action_theme_dark = QAction("&Dark Mode (Default)", self, checkable=True)
        self.action_theme_dark.setChecked(True)
        self.action_theme_dark.triggered.connect(lambda: self.set_theme("dark"))

        self.action_theme_light = QAction("&Light Mode", self, checkable=True)
        self.action_theme_light.triggered.connect(lambda: self.set_theme("light"))

        theme_group.addAction(self.action_theme_dark)
        theme_group.addAction(self.action_theme_light)
        theme_menu.addAction(self.action_theme_dark)
        theme_menu.addAction(self.action_theme_light)

        # Help Menu
        help_menu = menu_bar.addMenu("&Help")
        about_act = QAction(f"&About {__app_name__}", self)
        about_act.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_act)

    def _build_status_bar(self) -> None:
        status_bar = QStatusBar(self)
        self.setStatusBar(status_bar)

        self.status_message_label = QLabel("Ready — Phase 1 Workstation Foundation", self)
        self.device_badge = QLabel("DEVICE: CPU", self)
        self.device_badge.setObjectName("TelemetryBadge")

        self.cpu_badge = QLabel("CPU: --%", self)
        self.cpu_badge.setObjectName("TelemetryBadge")

        self.ram_badge = QLabel("RAM: -- / -- GB (--%)", self)
        self.ram_badge.setObjectName("TelemetryBadge")

        status_bar.addWidget(self.status_message_label, 1)
        status_bar.addPermanentWidget(self.device_badge)
        status_bar.addPermanentWidget(self.cpu_badge)
        status_bar.addPermanentWidget(self.ram_badge)

    def set_theme(self, theme: ThemeName) -> None:
        """Switch the application stylesheet between dark and light workstation modes."""
        self.current_theme = theme
        app = QApplication.instance()
        if isinstance(app, QApplication):
            apply_theme(app, theme)

        self.action_theme_dark.setChecked(theme == "dark")
        self.action_theme_light.setChecked(theme == "light")
        self.status_message_label.setText(f"Theme switched to {theme.title()} Mode")
        logger.info("Workstation theme switched to %s", theme)

    def reset_layout(self) -> None:
        """Restore all dock widgets to their default startup arrangement."""
        self.restoreState(self._initial_dock_state)
        for dock in self.docks.values():
            dock.show()
        self.status_message_label.setText("Workstation layout restored to default")

    def refresh_hardware_telemetry(self) -> HardwareSnapshot:
        """Poll HardwareMonitor and update the status bar and Processing Monitor dock."""
        snapshot = self.hardware_monitor.capture_snapshot()
        device_tag = "CUDA" if snapshot.cuda_available else "CPU-SAFE"
        self.device_badge.setText(f"MODE: {device_tag}")
        self.cpu_badge.setText(f"CPU: {snapshot.cpu_percent:.1f}%")

        ram_used_gb = max(0.0, snapshot.ram_total_gb - snapshot.ram_available_gb)
        self.ram_badge.setText(
            f"RAM: {ram_used_gb:.1f}/{snapshot.ram_total_gb:.1f} GB "
            f"({snapshot.ram_used_percent:.1f}%)"
        )

        target_obj_name = "TelemetryWarning" if snapshot.ram_warning else "TelemetryBadge"
        if self.ram_badge.objectName() != target_obj_name:
            self.ram_badge.setObjectName(target_obj_name)
            self.ram_badge.style().unpolish(self.ram_badge)
            self.ram_badge.style().polish(self.ram_badge)

        self.processing_monitor.update_telemetry(snapshot)
        return snapshot

    def show_about_dialog(self) -> None:
        """Display application version and architecture information."""
        QMessageBox.about(
            self,
            f"About {__app_name__}",
            (
                f"<h3>{__app_name__} v{__version__}</h3>"
                "<p>AI-powered music reconstruction, source separation, automatic music "
                "transcription, virtual instrumentation, audio restoration, and DAW.</p>"
                "<p><b>Milestone:</b> Phase 1 — Workstation Shell &amp; Core Foundation<br>"
                "<b>GUI Framework:</b> PySide6 (Qt6)</p>"
            ),
        )

    def closeEvent(self, event: QCloseEvent) -> None:
        """Stop background UI timers cleanly before closing the window."""
        if self.telemetry_timer.isActive():
            self.telemetry_timer.stop()
        logger.info("Closing LamiosMainWindow")
        super().closeEvent(event)

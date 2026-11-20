"""Modular workstation workspace tabs and dockable panel widgets for LAMIOS Studio."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QVBoxLayout,
    QWidget,
)

from lamios import __app_name__, __schema_version__, __version__
from lamios.core import AppConfig, HardwareSnapshot


class PlaceholderPanel(QWidget):
    """Structured placeholder panel for subsystems scheduled in upcoming phases."""

    def __init__(
        self,
        title: str,
        phase_label: str,
        description: str,
        capabilities: list[str],
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(16, 16, 16, 16)
        root_layout.setSpacing(12)

        card = QFrame(self)
        card.setObjectName("WorkspaceCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 18, 20, 18)
        card_layout.setSpacing(10)

        header_row = QHBoxLayout()
        title_label = QLabel(title, card)
        title_label.setObjectName("TitleLabel")
        badge_label = QLabel(phase_label, card)
        badge_label.setObjectName("BadgeLabel")
        header_row.addWidget(title_label)
        header_row.addStretch(1)
        header_row.addWidget(badge_label)

        desc_label = QLabel(description, card)
        desc_label.setObjectName("SubtitleLabel")
        desc_label.setWordWrap(True)

        card_layout.addLayout(header_row)
        card_layout.addWidget(desc_label)

        for item in capabilities:
            item_label = QLabel(f"•  {item}", card)
            item_label.setWordWrap(True)
            card_layout.addWidget(item_label)

        card_layout.addStretch(1)
        root_layout.addWidget(card)
        root_layout.addStretch(1)


class ProjectDashboardPanel(QWidget):
    """Landing dashboard displaying verified application version, config, and pipeline status."""

    def __init__(self, config: AppConfig, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        hero = QFrame(self)
        hero.setObjectName("WorkspaceCard")
        hero_layout = QVBoxLayout(hero)
        hero_layout.setContentsMargins(24, 20, 24, 20)
        hero_layout.setSpacing(8)

        title = QLabel(f"{__app_name__}  v{__version__}", hero)
        title.setObjectName("TitleLabel")
        subtitle = QLabel(
            "AI-Powered Music Reconstruction, Hierarchical Source Separation, "
            "Automatic Music Transcription, and Digital Audio Workstation",
            hero,
        )
        subtitle.setObjectName("SubtitleLabel")
        subtitle.setWordWrap(True)

        pipeline_label = QLabel(
            "Pipeline: Original Song → Source Detection → Separation → Transcription "
            "→ Editable Multitrack Project → Sound Redesign → Mixing → Export",
            hero,
        )
        pipeline_label.setWordWrap(True)

        hero_layout.addWidget(title)
        hero_layout.addWidget(subtitle)
        hero_layout.addWidget(pipeline_label)
        layout.addWidget(hero)

        env_card = QFrame(self)
        env_card.setObjectName("WorkspaceCard")
        grid = QGridLayout(env_card)
        grid.setContentsMargins(20, 16, 20, 16)
        grid.setHorizontalSpacing(24)
        grid.setVerticalSpacing(8)

        rows = [
            ("Active Build Milestone:", "Phase 1 — Workstation Shell & Core Foundation"),
            ("Core Data Schema Version:", __schema_version__),
            ("Execution Device Default:", f"{config.default_device.upper()} (CPU-Safe Mode)"),
            ("Quality Profile:", config.quality_mode.title()),
            ("RAM Safety Threshold:", f"{config.max_ram_usage_percent:.0f}%"),
            ("Audio Chunk Window:", f"{config.chunk_duration_seconds} seconds"),
            ("Model Unload After Stage:", "Enabled" if config.unload_models_after_stage else "Off"),
            ("Next Implementation Phase:", "Phase 2 — Audio Import, Decoding, Waveform & Playback"),
        ]
        for idx, (label_text, value_text) in enumerate(rows):
            key_lbl = QLabel(label_text, env_card)
            key_lbl.setObjectName("SubtitleLabel")
            val_lbl = QLabel(value_text, env_card)
            val_lbl.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            grid.addWidget(key_lbl, idx, 0)
            grid.addWidget(val_lbl, idx, 1)
        grid.setColumnStretch(1, 1)

        layout.addWidget(env_card)
        layout.addStretch(1)


class ProcessingMonitorPanel(QWidget):
    """Live hardware resource and background processing monitor dock widget."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        self.stage_label = QLabel("Processing Stage: Idle (Ready for Audio Import)", self)
        self.device_label = QLabel("Execution Device: Detecting...", self)
        self.device_label.setObjectName("SubtitleLabel")

        self.cpu_label = QLabel("CPU Usage: --%", self)
        self.cpu_bar = QProgressBar(self)
        self.cpu_bar.setRange(0, 100)
        self.cpu_bar.setValue(0)
        self.cpu_bar.setTextVisible(True)

        self.ram_label = QLabel("System RAM: -- / -- GB (--%)", self)
        self.ram_bar = QProgressBar(self)
        self.ram_bar.setRange(0, 100)
        self.ram_bar.setValue(0)
        self.ram_bar.setTextVisible(True)

        layout.addWidget(self.stage_label)
        layout.addWidget(self.device_label)
        layout.addWidget(self.cpu_label)
        layout.addWidget(self.cpu_bar)
        layout.addWidget(self.ram_label)
        layout.addWidget(self.ram_bar)
        layout.addStretch(1)

    def update_telemetry(self, snapshot: HardwareSnapshot) -> None:
        """Refresh CPU, RAM, and execution device indicators from a HardwareSnapshot."""
        device_text = (
            "CUDA GPU Accelerated" if snapshot.cuda_available else "CPU-Safe Mode (No CUDA GPU)"
        )
        self.device_label.setText(
            f"Execution Device: {device_text}  |  "
            f"Cores: {snapshot.cpu_physical_cores}P/{snapshot.cpu_logical_cores}L"
        )

        cpu_int = int(round(snapshot.cpu_percent))
        self.cpu_label.setText(f"CPU Usage: {snapshot.cpu_percent:.1f}%")
        self.cpu_bar.setValue(max(0, min(100, cpu_int)))

        ram_used_gb = max(0.0, snapshot.ram_total_gb - snapshot.ram_available_gb)
        ram_int = int(round(snapshot.ram_used_percent))
        warning_suffix = "  [HIGH RAM WARNING]" if snapshot.ram_warning else ""
        self.ram_label.setText(
            f"System RAM: {ram_used_gb:.1f} / {snapshot.ram_total_gb:.1f} GB "
            f"({snapshot.ram_used_percent:.1f}%){warning_suffix}"
        )
        self.ram_bar.setValue(max(0, min(100, ram_int)))

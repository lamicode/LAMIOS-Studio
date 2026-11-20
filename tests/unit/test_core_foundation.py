"""Unit tests for Phase 1, Task 1.1: config, logging, hardware telemetry, and core data models."""

from __future__ import annotations

from pathlib import Path

import pytest

from lamios import __app_name__, __schema_version__, __version__
from lamios.core import (
    AppConfig,
    AudioAssetRef,
    DrumEvent,
    HardwareMonitor,
    NoteEvent,
    StemArtifact,
    TrackMetadata,
    configure_logging,
    get_logger,
    load_config,
    samples_to_seconds,
    seconds_to_samples,
)


def test_package_metadata() -> None:
    assert __app_name__ == "LAMIOS Studio"
    assert __version__ == "0.1.0"
    assert __schema_version__ == "1.0.0"


def test_load_config_defaults_and_env_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    for key in (
        "LAMIOS_ENV",
        "LAMIOS_LOG_LEVEL",
        "LAMIOS_DEFAULT_DEVICE",
        "LAMIOS_QUALITY_MODE",
        "LAMIOS_MAX_RAM_USAGE_PERCENT",
        "LAMIOS_CHUNK_DURATION_SECONDS",
    ):
        monkeypatch.delenv(key, raising=False)

    env_file = tmp_path / ".env"
    env_file.write_text(
        "LAMIOS_LOG_LEVEL=DEBUG\n"
        "LAMIOS_DEFAULT_DEVICE=cpu\n"
        "LAMIOS_CHUNK_DURATION_SECONDS=20\n",
        encoding="utf-8",
    )

    cfg = load_config(project_root=tmp_path)
    assert isinstance(cfg, AppConfig)
    assert cfg.log_level == "DEBUG"
    assert cfg.default_device == "cpu"
    assert cfg.chunk_duration_seconds == 20
    assert cfg.max_ram_usage_percent == 75.0
    assert cfg.unload_models_after_stage is True

    cfg.ensure_runtime_directories()
    assert cfg.models_dir.is_dir()
    assert cfg.temp_dir.is_dir()
    assert cfg.logs_dir.is_dir()


def test_configure_logging_creates_log_file(tmp_path: Path) -> None:
    logs_dir = tmp_path / "logs"
    logger = configure_logging(logs_dir=logs_dir, log_level="INFO")
    child = get_logger("core.test")
    child.info("Foundation test log entry")

    for handler in logger.handlers:
        handler.flush()

    log_file = logs_dir / "lamios.log"
    assert log_file.is_file()
    content = log_file.read_text(encoding="utf-8")
    assert "LAMIOS logging initialized" in content
    assert "Foundation test log entry" in content


def test_hardware_monitor_captures_valid_snapshot() -> None:
    monitor = HardwareMonitor(ram_warning_threshold_percent=75.0)
    snapshot = monitor.capture_snapshot()

    assert snapshot.cpu_physical_cores >= 1
    assert snapshot.cpu_logical_cores >= snapshot.cpu_physical_cores
    assert snapshot.ram_total_gb > 0.0
    assert 0.0 <= snapshot.ram_used_percent <= 100.0
    assert snapshot.recommended_device in {"cpu", "cuda"}


def test_sample_time_conversion_roundtrip() -> None:
    sample_rate = 44100
    assert samples_to_seconds(44100, sample_rate) == pytest.approx(1.0)
    assert seconds_to_samples(1.5, sample_rate) == 66150

    with pytest.raises(ValueError):
        samples_to_seconds(-1, sample_rate)
    with pytest.raises(ValueError):
        seconds_to_samples(1.0, 0)


def test_audio_asset_and_stem_artifact_validation() -> None:
    asset = AudioAssetRef(
        role="broad_stem",
        relative_path="audio/stems_broad/vocals.wav",
        sample_rate=48000,
        channels=2,
        total_samples=96000,
    )
    assert asset.duration_seconds == pytest.approx(2.0)

    stem = StemArtifact(
        audio_ref=asset,
        instrument_family="vocals",
        specific_instrument="lead_vocal",
        classification_confidence=0.92,
        separation_confidence=0.88,
        model_provenance="sep_htdemucs_v4",
    )
    assert stem.specific_instrument == "lead_vocal"

    with pytest.raises(ValueError):
        StemArtifact(
            audio_ref=asset,
            instrument_family="vocals",
            specific_instrument="lead_vocal",
            classification_confidence=1.5,
            separation_confidence=0.8,
            model_provenance="sep_htdemucs_v4",
        )


def test_note_event_and_drum_event_contracts() -> None:
    note = NoteEvent(
        track_id="trk_1",
        stem_id="stm_1",
        instrument_id="piano_acoustic",
        pitch_midi=69,
        fundamental_hz=440.0,
        start_sample=44100,
        end_sample=88200,
        velocity=0.85,
        confidence=0.95,
        model_provenance="amt_basic_pitch",
    )
    assert note.duration_samples == 44100

    with pytest.raises(ValueError):
        NoteEvent(
            track_id="trk_1",
            stem_id="stm_1",
            instrument_id="piano_acoustic",
            pitch_midi=69,
            fundamental_hz=440.0,
            start_sample=88200,
            end_sample=44100,
            velocity=0.85,
            confidence=0.95,
            model_provenance="amt_basic_pitch",
        )

    drum = DrumEvent(
        track_id="trk_2",
        stem_id="stm_2",
        drum_class="kick",
        onset_sample=22050,
        velocity=0.9,
        confidence=0.91,
        timing_offset_samples=-50,
    )
    assert drum.effective_onset_sample == 22000


def test_track_metadata_validation() -> None:
    track = TrackMetadata(
        name="Track 01 — Lead Vocal",
        instrument_family="vocals",
        specific_instrument="lead_vocal",
        pan=-0.25,
        playback_mode="blended",
        blend_ratio=0.5,
    )
    assert track.pan == -0.25
    assert track.playback_mode == "blended"

    with pytest.raises(ValueError):
        TrackMetadata(
            name="Invalid Pan Track",
            instrument_family="guitars",
            specific_instrument="acoustic_guitar",
            pan=1.5,
        )

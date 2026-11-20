"""Authoritative versioned data contracts for LAMIOS Studio.

All timing positions use integer sample indices anchored to the project's
original audio sample rate to guarantee zero drift across stems, notes, and exports.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal
from uuid import uuid4

AudioRole = Literal["original", "broad_stem", "fine_stem", "residual", "restored"]
ArticulationType = Literal["normal", "staccato", "legato", "vibrato", "slide"]
EditStatus = Literal["raw_ai", "fused", "user_modified", "user_locked"]
PlaybackSourceMode = Literal["original_stem", "reconstructed_instrument", "blended"]

VALID_AUDIO_ROLES = {"original", "broad_stem", "fine_stem", "residual", "restored"}
VALID_ARTICULATIONS = {"normal", "staccato", "legato", "vibrato", "slide"}
VALID_EDIT_STATUSES = {"raw_ai", "fused", "user_modified", "user_locked"}
VALID_PLAYBACK_MODES = {"original_stem", "reconstructed_instrument", "blended"}


def new_id() -> str:
    """Generate a unique UUID4 string identifier."""
    return str(uuid4())


def samples_to_seconds(sample_pos: int, sample_rate: int) -> float:
    """Convert an integer sample position into seconds."""
    if sample_rate <= 0:
        raise ValueError(f"sample_rate must be positive, got {sample_rate}")
    if sample_pos < 0:
        raise ValueError(f"sample_pos cannot be negative, got {sample_pos}")
    return sample_pos / float(sample_rate)


def seconds_to_samples(time_seconds: float, sample_rate: int) -> int:
    """Convert time in seconds into the nearest authoritative integer sample index."""
    if sample_rate <= 0:
        raise ValueError(f"sample_rate must be positive, got {sample_rate}")
    if time_seconds < 0.0:
        raise ValueError(f"time_seconds cannot be negative, got {time_seconds}")
    return int(round(time_seconds * sample_rate))


def _validate_unit_interval(value: float, field_name: str) -> None:
    if not (0.0 <= value <= 1.0):
        raise ValueError(f"{field_name} must be between 0.0 and 1.0, got {value}")


@dataclass(frozen=True)
class AudioAssetRef:
    """Immutable metadata reference to an audio file stored inside a .lamios project."""

    role: AudioRole
    relative_path: str
    sample_rate: int
    channels: int
    total_samples: int
    peak_dbfs: float = 0.0
    rms_dbfs: float = -18.0
    sha256_checksum: str = ""
    asset_id: str = field(default_factory=new_id)

    def __post_init__(self) -> None:
        if self.role not in VALID_AUDIO_ROLES:
            raise ValueError(f"Invalid audio role: {self.role!r}")
        if not self.relative_path.strip():
            raise ValueError("relative_path cannot be empty")
        if self.sample_rate <= 0:
            raise ValueError(f"sample_rate must be positive, got {self.sample_rate}")
        if self.channels <= 0:
            raise ValueError(f"channels must be positive, got {self.channels}")
        if self.total_samples < 0:
            raise ValueError(f"total_samples cannot be negative, got {self.total_samples}")

    @property
    def duration_seconds(self) -> float:
        """Exact audio duration in seconds derived from sample count and sample rate."""
        return samples_to_seconds(self.total_samples, self.sample_rate)


@dataclass
class StemArtifact:
    """Represents a separated broad, fine, or residual audio stem with quality telemetry."""

    audio_ref: AudioAssetRef
    instrument_family: str
    specific_instrument: str
    classification_confidence: float
    separation_confidence: float
    model_provenance: str
    parent_stem_id: str | None = None
    reconstruction_error_db: float | None = None
    stem_id: str = field(default_factory=new_id)

    def __post_init__(self) -> None:
        _validate_unit_interval(self.classification_confidence, "classification_confidence")
        _validate_unit_interval(self.separation_confidence, "separation_confidence")
        if not self.instrument_family.strip():
            raise ValueError("instrument_family cannot be empty")
        if not self.specific_instrument.strip():
            raise ValueError("specific_instrument cannot be empty")
        if not self.model_provenance.strip():
            raise ValueError("model_provenance cannot be empty")


@dataclass
class NoteEvent:
    """Internal musical note event anchored to authoritative sample indices (MIDI-independent)."""

    track_id: str
    stem_id: str
    instrument_id: str
    pitch_midi: int
    fundamental_hz: float
    start_sample: int
    end_sample: int
    velocity: float
    confidence: float
    model_provenance: str
    pitch_curve_cents: list[tuple[int, float]] = field(default_factory=list)
    expression_curve: list[tuple[int, float]] = field(default_factory=list)
    articulation: ArticulationType = "normal"
    edit_status: EditStatus = "raw_ai"
    note_id: str = field(default_factory=new_id)

    def __post_init__(self) -> None:
        if not (0 <= self.pitch_midi <= 127):
            raise ValueError(f"pitch_midi must be in 0..127, got {self.pitch_midi}")
        if self.fundamental_hz <= 0.0:
            raise ValueError(f"fundamental_hz must be positive, got {self.fundamental_hz}")
        if self.start_sample < 0:
            raise ValueError(f"start_sample cannot be negative, got {self.start_sample}")
        if self.end_sample <= self.start_sample:
            raise ValueError(
                f"end_sample ({self.end_sample}) must be strictly greater than "
                f"start_sample ({self.start_sample})"
            )
        _validate_unit_interval(self.velocity, "velocity")
        _validate_unit_interval(self.confidence, "confidence")
        if self.articulation not in VALID_ARTICULATIONS:
            raise ValueError(f"Invalid articulation: {self.articulation!r}")
        if self.edit_status not in VALID_EDIT_STATUSES:
            raise ValueError(f"Invalid edit_status: {self.edit_status!r}")

    @property
    def duration_samples(self) -> int:
        """Exact note duration in audio samples."""
        return self.end_sample - self.start_sample


@dataclass
class DrumEvent:
    """Percussive hit event stored independently from pitched melodic notes."""

    track_id: str
    stem_id: str
    drum_class: str
    onset_sample: int
    velocity: float
    confidence: float
    sample_override_id: str | None = None
    timing_offset_samples: int = 0
    edit_status: EditStatus = "raw_ai"
    event_id: str = field(default_factory=new_id)

    def __post_init__(self) -> None:
        if not self.drum_class.strip():
            raise ValueError("drum_class cannot be empty")
        if self.onset_sample < 0:
            raise ValueError(f"onset_sample cannot be negative, got {self.onset_sample}")
        _validate_unit_interval(self.velocity, "velocity")
        _validate_unit_interval(self.confidence, "confidence")
        if self.edit_status not in VALID_EDIT_STATUSES:
            raise ValueError(f"Invalid edit_status: {self.edit_status!r}")

    @property
    def effective_onset_sample(self) -> int:
        """Effective onset position after applying non-destructive timing/quantization offset."""
        return max(0, self.onset_sample + self.timing_offset_samples)


@dataclass
class TrackMetadata:
    """High-level state of a single track in a LAMIOS multitrack project."""

    name: str
    instrument_family: str
    specific_instrument: str
    color_hex: str = "#3B82F6"
    volume_db: float = 0.0
    pan: float = 0.0
    muted: bool = False
    soloed: bool = False
    playback_mode: PlaybackSourceMode = "original_stem"
    blend_ratio: float = 0.0
    track_id: str = field(default_factory=new_id)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Track name cannot be empty")
        if not (-1.0 <= self.pan <= 1.0):
            raise ValueError(f"pan must be between -1.0 and 1.0, got {self.pan}")
        if self.playback_mode not in VALID_PLAYBACK_MODES:
            raise ValueError(f"Invalid playback_mode: {self.playback_mode!r}")
        _validate_unit_interval(self.blend_ratio, "blend_ratio")

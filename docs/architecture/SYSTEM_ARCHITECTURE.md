# LAMIOS Studio — System Architecture & Core Data Contracts

**Document Version:** 1.0 (Phase 0 Baseline)

---

## 1. Architectural Overview & Thread/Process Isolation

To guarantee a freeze-free GUI and glitch-free audio on a 4-core CPU with 15.8 GB RAM, LAMIOS Studio enforces strict boundary isolation across three execution tiers:

1. **GUI & Presentation Tier (`src/lamios/gui/` — Main Qt Thread):**
   * Built with **PySide6**.
   * Renders dockable panels, waveforms, hardware-accelerated `QGraphicsView` piano rolls, vocal pitch curves, drum lanes, and mixer strips.
   * Communicates exclusively with `src/lamios/core/` and `src/lamios/project/` data models via Qt Signals/Slots and command objects (`QUndoCommand`).
2. **Real-Time Audio & Playback Tier (`src/lamios/audio/`, `src/lamios/playback/`, `src/lamios/mixer/`):**
   * Uses `sounddevice` (PortAudio / Windows WASAPI) with pre-allocated lock-free ring buffers.
   * Zero Python memory allocation and zero AI inference inside real-time audio callbacks.
3. **Background DSP & AI Worker Tier (`src/lamios/workers/`):**
   * Executes DSP preprocessing, source separation, instrument classification, and automatic music transcription in isolated background worker processes/threads with cancellation tokens, progress telemetry, and explicit memory cleanup (`gc.collect()`).

---

## 2. Authoritative Sample Timeline Specification

All timing across LAMIOS Studio is anchored to an integer **Original Sample Index (`sample_pos: int`)** relative to the project's authoritative sample rate (`project_sample_rate: int`, e.g., `44100` or `48000` Hz):

* **Conversion Rule:** `time_seconds = sample_pos / project_sample_rate`
* **Resampling Compensation:** If an AI model requires a 16,000 Hz or 22,050 Hz input internally, the model adapter converts output frame indices back into `project_sample_rate` integer sample positions before returning results.
* **Zero-Drift Guarantee:** Every separated stem must match the exact sample count (`total_samples: int`) of the original imported recording.

---

## 3. Core Versioned Data Schemas (`src/lamios/core/models.py`)

### 3.1 `AudioAssetRef`
```python
@dataclass(frozen=True)
class AudioAssetRef:
    asset_id: str                # UUID4
    role: str                    # "original" | "broad_stem" | "fine_stem" | "residual" | "restored"
    relative_path: str           # Path inside .lamios project container (lossless WAV/FLAC)
    sample_rate: int             # e.g., 44100 or 48000
    channels: int                # 1 (mono) or 2 (stereo)
    total_samples: int           # Exact sample frame count
    peak_dbfs: float
    rms_dbfs: float
    sha256_checksum: str
```

### 3.2 `StemArtifact`
```python
@dataclass
class StemArtifact:
    stem_id: str                 # UUID4
    parent_stem_id: Optional[str]# None for broad separation; parent stem UUID for hierarchical sub-stems
    audio_ref: AudioAssetRef
    instrument_family: str       # e.g., "vocals", "drums", "bass", "guitars", "keyboards", "strings", "unresolved"
    specific_instrument: str     # e.g., "lead_vocal", "acoustic_guitar", "kick", "unresolved_group"
    classification_confidence: float  # 0.0 to 1.0
    separation_confidence: float      # 0.0 to 1.0
    reconstruction_error_db: Optional[float]
    model_provenance: str        # Adapter ID & version used
```

### 3.3 `NoteEvent` (Internal Musical Performance Schema — Independent of MIDI)
```python
@dataclass
class NoteEvent:
    note_id: str                 # UUID4
    track_id: str
    stem_id: str
    instrument_id: str
    pitch_midi: int              # 0..127 integer pitch center
    fundamental_hz: float        # Exact detected fundamental frequency in Hz
    start_sample: int            # Authoritative onset sample index
    end_sample: int              # Authoritative offset sample index
    velocity: float              # Normalized 0.0 to 1.0 (mapped to 1..127 only on MIDI export)
    confidence: float            # 0.0 to 1.0
    pitch_curve_cents: list[tuple[int, float]]  # [(sample_offset, cents_deviation), ...]
    expression_curve: list[tuple[int, float]]   # [(sample_offset, normalized_gain), ...]
    articulation: str            # "normal" | "staccato" | "legato" | "vibrato" | "slide"
    model_provenance: str        # e.g., "basic_pitch_v1" | "crepe_v1" | "manual"
    edit_status: str             # "raw_ai" | "fused" | "user_modified" | "user_locked"
```

### 3.4 `DrumEvent`
```python
@dataclass
class DrumEvent:
    event_id: str                # UUID4
    track_id: str
    stem_id: str
    drum_class: str              # "kick" | "snare" | "hihat_closed" | "hihat_open" | "tom" | "cymbal" | "percussion"
    onset_sample: int            # Authoritative transient sample position
    velocity: float              # 0.0 to 1.0
    confidence: float            # 0.0 to 1.0
    sample_override_id: Optional[str]
    timing_offset_samples: int   # Non-destructive quantization/swing offset
    edit_status: str             # "raw_ai" | "user_modified"
```

---

## 4. Native Project Container Format (`.lamios`)

A `.lamios` project is a structured, versioned directory bundle (or uncompressed ZIP container on export) containing:
```text
MySongProject.lamios/
├── manifest.json                # Schema version, sample rate, creation date, checksums
├── project.db                   # SQLite database storing tracks, NoteEvents, DrumEvents, chords, tempo map, undo history
├── audio/
│   ├── original/                # Immutable lossless original audio
│   ├── stems_broad/             # Broad separation stems + residual
│   ├── stems_fine/              # Sub-separated instrument/vocal/drum stems
│   └── restored/                # Non-destructive audio restoration outputs
└── backups/                     # Automatic transactional snapshots of project.db
```
Using **SQLite (`project.db`)** for note events, drum hits, automation points, and undo history allows instant querying and transactional saves without rewriting gigabytes of audio files on every `Ctrl+S`.

# LAMIOS STUDIO — UNIFIED MASTER SOFTWARE DEVELOPMENT BLUEPRINT
**Version 3.0 — Gemini Website Edition**
**Status:** Authoritative Master Specification

## 1. Product Vision & Transformation Pipeline
LAMIOS Studio is an advanced AI-powered music deconstruction, transcription, sound replacement, restoration, and digital audio workstation for Windows 11 (64-bit).

**Transformation Flow:**
`Original Song` → `Source Detection` → `Instrument & Vocal Separation` → `Musical Transcription` → `Editable Multitrack Project` → `Sound Redesign` → `Mixing` → `Export`

## 2. Three Fundamental Synchronized Representations
1. **Original Audio:** Immutable imported or recorded audio signal anchored to original sample indices.
2. **Separated Audio:** Individual instrument, vocal, percussion, or unresolved-group stems plus preserved residual audio.
3. **Musical Performance Data:** Sample-accurate internal representations of notes, drum hits, continuous pitch curves, expression, and music-theory structures. MIDI is strictly an optional export format and is never used as the internal storage format.

## 3. Layered 18-Stage Architecture
1. Audio Acquisition
2. Audio Decoding
3. Lossless Working Representation
4. DSP Preprocessing
5. Musical Structure Analysis
6. Instrument and Vocal Activity Detection
7. Hierarchical Source Separation
8. Source Classification
9. Specialized Transcription
10. Note-Event Fusion
11. Musical Expression Reconstruction
12. Music Theory Analysis
13. Multitrack Project Generation
14. Piano-Roll and Waveform Editing
15. Sound Generation (Virtual Instruments & SoundFonts)
16. Audio Effects & Audio Restoration
17. Mixing and Playback
18. Audio, Stem, and Optional MIDI Export

## 4. Development Phases (Phases 0–19)
* **Phase 0:** Architecture and feasibility
* **Phase 1:** Environment and application foundation
* **Phase 2:** Audio import and playback
* **Phase 3:** Multitrack project system
* **Phase 4:** DSP and musical analysis
* **Phase 5:** Broad source separation
* **Phase 6:** Instrument detection and fine separation
* **Phase 7:** Automatic transcription
* **Phase 8:** Piano-roll editor
* **Phase 9:** Drum transcription
* **Phase 10:** Vocal analysis
* **Phase 11:** Music theory
* **Phase 12:** Virtual instruments
* **Phase 13:** Audio restoration
* **Phase 14:** Effects and mixer
* **Phase 15:** Live analysis
* **Phase 16:** Export
* **Phase 17:** Performance optimization
* **Phase 18:** Windows distribution
* **Phase 19:** Commercial readiness

## 5. Non-Negotiable Engineering Honesty
* Measure separation and transcription quality; expose confidence indicators in the GUI.
* Preserve unresolved group stems and residual audio rather than fabricating fake clean stems.
* Never overwrite manual user edits silently during re-analysis.
* Maintain full responsiveness on the user's Windows 11 CPU baseline (Intel i7-1165G7, 16 GB RAM).

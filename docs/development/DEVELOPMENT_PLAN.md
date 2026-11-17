# LAMIOS Studio — Master Development Plan

| Phase | Milestone Name | Core Deliverables | Status |
|---|---|---|---|
| **Phase 0** | Architecture & Feasibility | Hardware/Python 3.10 audit, repo setup, blueprints, schemas, model & license registry | **In Progress (Task 0.2)** |
| **Phase 1** | Environment & App Foundation | `.venv` setup, `pyproject.toml`, logging, hardware monitor, PySide6 Dark Workstation Shell, `pytest` suite | Pending |
| **Phase 2** | Audio Import & Playback | Multi-format decoding, waveform viewer, WASAPI playback/seek, device selector, live recording | Pending |
| **Phase 3** | Multitrack Project System | Track management, synchronized multitrack playback, `.lamios` SQLite/manifest save/load, Undo/Redo | Pending |
| **Phase 4** | DSP & Musical Analysis | STFT/CQT, DC/noise/gain audit, onset/beat/downbeat tracking, tempo & key estimation | Pending |
| **Phase 5** | Broad Source Separation | HTDemucs / RoFormer adapter, 4–6 stem separation, residual preservation, SDR/leakage telemetry | Pending |
| **Phase 6** | Instrument Detection & Fine Separation | CLAP + spectral taxonomy classifier, source activity detection, confidence-aware sub-separation | Pending |
| **Phase 7** | Automatic Music Transcription | Model router, polyphonic/monophonic/piano/bass adapters, `NoteEvent` generation, Note Fusion engine | Pending |
| **Phase 8** | Piano-Roll Editor | Hardware-accelerated multitrack piano roll, note editing, velocity/pitch curves, confidence overlays | Pending |
| **Phase 9** | Drum Transcription & Sub-Separation | Drum sub-stems, transient hit detection, drum lane editor, quantization, sample replacement | Pending |
| **Phase 10** | Vocal & Singer Analysis | Vocal activity, lead/backing separation, singer embeddings/clustering, vocal pitch curve editor | Pending |
| **Phase 11** | Music Theory Engine | Chord recognition (major/minor/7th/ext/slash), key/scale grids, tempo maps, time signatures | Pending |
| **Phase 12** | Virtual Instruments | FluidSynth / SF2 / SFZ synth playback, ADSR/filter controls, original vs. reconstructed stem blending | Pending |
| **Phase 13** | Audio Restoration | Spectral noise reduction, de-reverb, de-harshing, 130 Hz mono-bass cleanup, transient shaping, A/B bypass | Pending |
| **Phase 14** | Audio Effects & Mixer | Per-track effects chain, parametric EQ, dynamics, reverb/delay, buses, automation lanes | Pending |
| **Phase 15** | Live Analysis Mode | Low-latency streaming pitch/chord detection, provisional live piano roll | Pending |
| **Phase 16** | Export & DAW Interoperability | WAV/FLAC/MP3 stem & master export, optional Type 1 / per-track / MPE MIDI export | Pending |
| **Phase 17** | Performance Optimization | Chunked RAM optimization, disk-backed buffers, caching, checkpoint resume | Pending |
| **Phase 18** | Windows Distribution | PyInstaller/Nuitka packaging, Windows installer, on-demand model downloader | Pending |
| **Phase 19** | Commercial Readiness | Full QA benchmark pass, license inventory audit, user documentation | Pending |

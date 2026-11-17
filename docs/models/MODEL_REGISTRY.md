# LAMIOS Studio — AI Model & DSP Dependency Registry

This registry tracks all candidate AI models and DSP engines, their resource budgets on our **Intel Core i7-1165G7 (15.8 GB RAM, CPU-Safe)** baseline, and their licensing status.

## 1. Licensing Policy for Development vs. Commercial Release
* **During Development & Personal Use:** Zero licensing restrictions apply on your local computer. We can use both permissive (MIT/BSD/Apache 2.0/LGPL) and copyleft/research (GPLv3 / CC-BY-NC) libraries and weights to achieve maximum audio quality immediately.
* **Adapter Isolation Guarantee:** Every model and DSP backend is wrapped inside a modular adapter class. If you later decide to sell LAMIOS Studio commercially, any `GPLv3` or `CC-BY-NC` adapter can be toggled off or swapped without rewriting the GUI, project format, or core pipeline.

---

## 2. Candidate AI Model Registry

| Task Domain | Model / Library Name | Adapter ID | Code License | Weights License | CPU-Safe (16GB RAM) | Est. Peak RAM | Isolation / Runtime |
|---|---|---|---|---|---|---|---|
| **Broad Separation** | HTDemucs (`htdemucs` / `htdemucs_6s`) | `sep_htdemucs_v4` | MIT | MIT | Yes (Chunked 30s) | ~2.8 GB | PyTorch CPU |
| **Vocal / Mel-Band Separation** | Mel-Band RoFormer / MDX-Net (ONNX) | `sep_mel_roformer` | MIT | MIT / Research | Yes (Chunked) | ~3.5 GB | PyTorch / ONNX Runtime |
| **Instrument Classification** | LAION-CLAP + Spectral Descriptors | `cls_clap_hybrid` | MIT / CC0 | Apache 2.0 | Yes | ~1.5 GB | PyTorch / librosa |
| **Polyphonic Transcription** | Spotify Basic Pitch | `amt_basic_pitch` | Apache 2.0 | Apache 2.0 | Yes (Fast on CPU) | ~0.8 GB | ONNX Runtime CPU |
| **Monophonic & Vocal Pitch** | `torchcrepe` / `librosa.pyin` | `amt_crepe_pyin` | MIT / ISC | MIT | Yes | ~0.9 GB | PyTorch CPU / NumPy |
| **Piano Transcription** | ByteDance Piano Transcription | `amt_piano_bd` | MIT | CC-BY-NC-4.0 | Yes (Chunked) | ~2.2 GB | PyTorch CPU / ONNX |
| **Drum Transcription** | ADTOF-PyTorch / Onset Transient Classifier | `amt_drums_adtof` | MIT / BSD | MIT / Research | Yes | ~1.0 GB | PyTorch / SciPy |
| **Singer Embeddings** | SpeechBrain ECAPA-TDNN | `voc_ecapa_tdnn` | Apache 2.0 | Apache 2.0 | Yes | ~1.1 GB | PyTorch CPU |
| **Virtual Instruments** | FluidSynth (`pyfluidsynth`) | `syn_fluidsynth` | LGPLv2.1 | SoundFont dependent | Yes (Real-time) | ~0.3 GB | Native C DLL |
| **Effects & Mastering** | `scipy.signal` + `pedalboard` (Optional Adapter) | `fx_hybrid_chain` | BSD / GPLv3 | N/A | Yes (Real-time) | ~0.2 GB | C++ / NumPy |

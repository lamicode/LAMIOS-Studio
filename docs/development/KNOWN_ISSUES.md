# LAMIOS Studio — Known Issues & Hardware Constraints

| ID | Category | Description | Mitigation Strategy | Status |
|---|---|---|---|---|
| **HW-01** | GPU / CUDA | Host PC uses Intel Iris Xe integrated graphics (no NVIDIA CUDA GPU). | Default all PyTorch and ONNX Runtime adapters to CPU execution with multi-threading (`torch.set_num_threads(4)`) and chunked inference. | Active Design Rule |
| **HW-02** | System RAM | Host PC has 15.8 GB total RAM; loading multiple large separation & transcription models simultaneously could cause memory pressure. | Enforce sequential stage execution with explicit `del model` and `gc.collect()` between stages. | Active Design Rule |
| **ENV-01** | Multiple Python Versions | System has Python 3.13, 3.12, and 3.10 installed. Python 3.13 lacks prebuilt wheels for several audio ML packages. | Always create the project virtual environment explicitly with `py -3.10 -m venv .venv`. | Resolved by Policy |

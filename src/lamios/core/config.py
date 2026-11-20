"""Application configuration loader with CPU-safe defaults for 16 GB RAM workstations."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    """Immutable runtime configuration for LAMIOS Studio."""

    env: str = "development"
    log_level: str = "INFO"
    default_device: str = "cpu"
    quality_mode: str = "balanced"
    max_ram_usage_percent: float = 75.0
    chunk_duration_seconds: int = 30
    unload_models_after_stage: bool = True
    project_root: Path = Path(".")
    models_dir: Path = Path("models/weights")
    temp_dir: Path = Path("temp")
    logs_dir: Path = Path("logs")

    def __post_init__(self) -> None:
        if self.default_device not in {"cpu", "cuda", "auto"}:
            raise ValueError(f"Unsupported default_device: {self.default_device!r}")
        if self.quality_mode not in {"fast", "balanced", "maximum", "cpu_safe"}:
            raise ValueError(f"Unsupported quality_mode: {self.quality_mode!r}")
        if not (10.0 <= self.max_ram_usage_percent <= 95.0):
            raise ValueError(
                "max_ram_usage_percent must be between 10.0 and 95.0, "
                f"got {self.max_ram_usage_percent}"
            )
        if self.chunk_duration_seconds <= 0:
            raise ValueError(
                f"chunk_duration_seconds must be positive, got {self.chunk_duration_seconds}"
            )

    def ensure_runtime_directories(self) -> None:
        """Create required local runtime directories if they do not exist."""
        for directory in (self.models_dir, self.temp_dir, self.logs_dir):
            directory.mkdir(parents=True, exist_ok=True)


def _parse_env_file(env_path: Path) -> dict[str, str]:
    """Parse simple KEY=VALUE pairs from a .env file without external dependencies."""
    values: dict[str, str] = {}
    if not env_path.is_file():
        return values

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        values[key.strip()] = val.strip().strip('"').strip("'")
    return values


def _parse_bool(raw: str, default: bool) -> bool:
    normalized = raw.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    return default


def load_config(project_root: Path | None = None) -> AppConfig:
    """Load LAMIOS Studio configuration from environment variables and optional .env file.

    Precedence: OS environment variables > .env file > built-in CPU-safe defaults.
    """
    root = (project_root or Path.cwd()).resolve()
    file_env = _parse_env_file(root / ".env")

    def get_val(key: str, default: str) -> str:
        return os.environ.get(key, file_env.get(key, default))

    def resolve_dir(raw_path: str) -> Path:
        candidate = Path(raw_path)
        return candidate if candidate.is_absolute() else (root / candidate).resolve()

    return AppConfig(
        env=get_val("LAMIOS_ENV", "development"),
        log_level=get_val("LAMIOS_LOG_LEVEL", "INFO").upper(),
        default_device=get_val("LAMIOS_DEFAULT_DEVICE", "cpu").lower(),
        quality_mode=get_val("LAMIOS_QUALITY_MODE", "balanced").lower(),
        max_ram_usage_percent=float(get_val("LAMIOS_MAX_RAM_USAGE_PERCENT", "75")),
        chunk_duration_seconds=int(get_val("LAMIOS_CHUNK_DURATION_SECONDS", "30")),
        unload_models_after_stage=_parse_bool(
            get_val("LAMIOS_UNLOAD_MODELS_AFTER_STAGE", "true"), default=True
        ),
        project_root=root,
        models_dir=resolve_dir(get_val("LAMIOS_MODELS_DIR", "./models/weights")),
        temp_dir=resolve_dir(get_val("LAMIOS_TEMP_DIR", "./temp")),
        logs_dir=resolve_dir(get_val("LAMIOS_LOGS_DIR", "./logs")),
    )

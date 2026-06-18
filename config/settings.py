import os
from pathlib import Path

# Resolve absolute paths relative to project root (AEVAR/)
BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
QUARANTINE_DIR = BASE_DIR / "data" / "quarantine"

# Create directories if they don't exist yet
for path in [RAW_DATA_DIR, PROCESSED_DATA_DIR, QUARANTINE_DIR]:
    path.mkdir(parents=True, exist_ok=True)
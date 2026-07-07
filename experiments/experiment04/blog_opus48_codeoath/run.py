#!/usr/bin/env python3
"""Entry point: start the local blog server.

Run with:  python run.py
Options:   python run.py --port 8080 --posts ./posts
"""

import sys
from pathlib import Path

# Make the package under src/ importable without installation.
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from blog.app import main  # noqa: E402 (import after sys.path setup)

if __name__ == "__main__":
    raise SystemExit(main())

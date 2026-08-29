#!/usr/bin/env python3
"""mg — Milbourne Group pipeline CLI. Run from anywhere in the repository."""
import signal
import sys
from pathlib import Path

# Operators pipe this into head/less; don't traceback on a closed pipe.
try:
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
except (AttributeError, ValueError):
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent / "tools"))
from mg.cli import main

try:
    sys.exit(main())
except BrokenPipeError:
    sys.exit(0)
except KeyboardInterrupt:
    sys.exit(130)

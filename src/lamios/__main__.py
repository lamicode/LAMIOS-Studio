"""Package entry point allowing execution via `python -m lamios`."""

from __future__ import annotations

import sys

from lamios.app.main import main

if __name__ == "__main__":
    sys.exit(main())

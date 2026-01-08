from __future__ import annotations

import sys
from pathlib import Path

REQUIRED_FILES = [
    Path("docs/assets/demo_output.txt"),
    Path("docs/assets/kpi_table.md"),
]


def main() -> None:
    missing = [str(path) for path in REQUIRED_FILES if not path.exists()]
    if missing:
        print("Faltan evidencias:")
        for path in missing:
            print(f"- {path}")
        sys.exit(1)

    empty = [str(path) for path in REQUIRED_FILES if path.stat().st_size == 0]
    if empty:
        print("Evidencias vacias:")
        for path in empty:
            print(f"- {path}")
        sys.exit(1)

    print("Wow audit OK")


if __name__ == "__main__":
    main()

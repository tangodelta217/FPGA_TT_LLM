from __future__ import annotations

import argparse
from pathlib import Path
import zipfile

DEFAULT_OUTPUT = Path("docs/indra_pack.zip")
INCLUDE_DIRS = [Path("docs/indra"), Path("docs/assets")]


def build_pack(output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for base_dir in INCLUDE_DIRS:
            if not base_dir.exists():
                continue
            for path in base_dir.rglob("*"):
                if path.is_file():
                    zf.write(path, path.as_posix())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Empaqueta docs para Indra.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Ruta del zip.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    build_pack(args.output)


if __name__ == "__main__":
    main()

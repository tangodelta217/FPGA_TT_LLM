from __future__ import annotations

from pathlib import Path
import sys

REQUIRED_DIRS = [
    Path("docs"),
    Path("docs/indra"),
    Path("docs/assets"),
    Path("ml"),
    Path("hw"),
    Path("hw/hls"),
    Path("hw/rtl"),
    Path("sw"),
    Path("scripts"),
    Path("tests"),
    Path(".github"),
    Path(".github/workflows"),
]

REQUIRED_FILES = [
    Path("LICENSE"),
    Path(".gitignore"),
    Path("SECURITY.md"),
    Path("CONTRIBUTING.md"),
    Path("CITATION.cff"),
    Path("requirements.txt"),
    Path("pyproject.toml"),
    Path("Makefile"),
    Path("README.md"),
    Path("docs/indra/onepager.md"),
    Path("docs/indra/pitchdeck.md"),
    Path("docs/indra/techbrief.md"),
    Path("docs/indra/evidence_pack.md"),
    Path("docs/indra/README.md"),
]


def main() -> None:
    missing_dirs = [str(path) for path in REQUIRED_DIRS if not path.is_dir()]
    missing_files = [str(path) for path in REQUIRED_FILES if not path.is_file()]

    if missing_dirs or missing_files:
        if missing_dirs:
            print("Directorios faltantes:")
            for path in missing_dirs:
                print(f"- {path}")
        if missing_files:
            print("Archivos faltantes:")
            for path in missing_files:
                print(f"- {path}")
        sys.exit(1)

    print("check_repo OK")


if __name__ == "__main__":
    main()

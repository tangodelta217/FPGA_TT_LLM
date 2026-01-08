from __future__ import annotations

import argparse
import zipfile
from pathlib import Path

DEFAULT_OUTPUT = Path("dist/indra_pack.zip")
INDEX_PATH = Path("dist/INDRA_PACK_INDEX.txt")

INDRA_DOCS_DIR = Path("docs/indra")

REQUIRED_FILES = [
    Path("README.md"),
    Path("docs/assets/demo_output.txt"),
    Path("docs/assets/bench_results.csv"),
    Path("docs/assets/bench_tradeoff.png"),
    Path("docs/assets/kpi_table.md"),
]

OPTIONAL_FILES = [
    Path("hw/README.md"),
    Path("docs/assets/register_map.md"),
    Path("docs/assets/hw_block_diagram.md"),
]


def build_index(included: list[Path]) -> None:
    lines = [
        "INDRA_PACK_INDEX",
        "",
        "Contenido:",
    ]
    for path in included:
        lines.append(f"- {path.as_posix()}")

    lines.extend(
        [
            "",
            "Como abrir:",
            "1) Leer README.md para contexto general.",
            "2) Revisar docs/indra/onepager.md, pitchdeck.md y techbrief.md.",
            "3) Ver evidencias en docs/assets/ y evidence_pack.md.",
        ]
    )

    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_pack(output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    docs = sorted(INDRA_DOCS_DIR.glob("*.md"))
    missing_docs = [str(path) for path in docs if not path.exists()]
    if not docs or missing_docs:
        raise FileNotFoundError("Faltan documentos Indra")

    missing_required = [str(path) for path in REQUIRED_FILES if not path.exists()]
    if missing_required:
        raise FileNotFoundError(f"Faltan archivos requeridos: {missing_required}")

    included = docs + REQUIRED_FILES
    for path in OPTIONAL_FILES:
        if path.exists():
            included.append(path)

    build_index(included)
    included.append(INDEX_PATH)

    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in included:
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

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

README_PATH = REPO_ROOT / "README.md"
INDRA_DOCS = [
    REPO_ROOT / "docs/indra/onepager.md",
    REPO_ROOT / "docs/indra/pitchdeck.md",
    REPO_ROOT / "docs/indra/techbrief.md",
    REPO_ROOT / "docs/indra/evidence_pack.md",
]
EVIDENCE_PATH = REPO_ROOT / "docs/indra/evidence_pack.md"

REQUIRED_README_SECTIONS = [
    "## Problema",
    "## Soluci\u00f3n",
    "## Quickstart",
    "## Arquitectura",
    "## Indra Package",
]

REQUIRED_README_LINKS = {
    "docs/indra/onepager.md",
    "docs/indra/pitchdeck.md",
    "docs/indra/techbrief.md",
    "docs/indra/evidence_pack.md",
}

REQUIRED_BENCH_LINKS = {
    "../assets/bench_tradeoff.png",
    "../assets/kpi_table.md",
}

REQUIRED_BENCH_OUTPUTS = [
    REPO_ROOT / "docs/assets/bench_tradeoff.png",
    REPO_ROOT / "docs/assets/kpi_table.md",
]
REQUIRED_DEMO_OUTPUT = REPO_ROOT / "docs/assets/demo_output.txt"

MAX_FILE_SIZE = 10 * 1024 * 1024

SKIP_DIRS = {".git", ".venv", "__pycache__", ".pytest_cache", ".ruff_cache"}


def run_command(cmd: list[str], label: str) -> None:
    result = subprocess.run(cmd, cwd=REPO_ROOT, check=False)
    if result.returncode != 0:
        raise RuntimeError(f"Fallo comando: {label}")


def run_make(target: str) -> None:
    if os.name == "nt" and (REPO_ROOT / "make.bat").exists():
        cmd = ["cmd.exe", "/c", "make.bat", target]
    elif shutil.which("make"):
        cmd = ["make", target]
    else:
        raise RuntimeError("make no disponible")
    run_command(cmd, f"make {target}")


def find_links(text: str) -> set[str]:
    return set(re.findall(r"\[[^\]]+\]\(([^)]+)\)", text))


def check_readme_sections() -> None:
    text = README_PATH.read_text(encoding="utf-8")
    missing = [section for section in REQUIRED_README_SECTIONS if section not in text]
    if missing:
        raise RuntimeError(f"README sin secciones requeridas: {missing}")

    links = find_links(text)
    missing_links = REQUIRED_README_LINKS - links
    if missing_links:
        raise RuntimeError(f"README sin links Indra Package: {sorted(missing_links)}")


def extract_kpis(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip().startswith("## KPI"):
            start = i + 1
            break
    if start is None:
        return []

    kpis: list[str] = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        if line.startswith("|") and "---" not in line:
            parts = [part.strip() for part in line.strip("|").split("|")]
            if parts and parts[0] != "KPI":
                kpis.append(parts[0])
    return kpis


def check_kpi_consistency() -> None:
    onepager = extract_kpis(REPO_ROOT / "docs/indra/onepager.md")
    techbrief = extract_kpis(REPO_ROOT / "docs/indra/techbrief.md")
    readme = extract_kpis(README_PATH)

    missing_in_techbrief = sorted(set(onepager) - set(techbrief))
    missing_in_readme = sorted(set(onepager) - set(readme))
    if missing_in_techbrief or missing_in_readme:
        raise RuntimeError(
            "KPIs inconsistentes. Faltan en techbrief o README: "
            f"techbrief={missing_in_techbrief}, README={missing_in_readme}"
        )


def check_links_local(paths: list[Path]) -> None:
    broken: list[str] = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for link in find_links(text):
            if link.startswith("http") or link.startswith("mailto:") or link.startswith("#"):
                continue
            target = (path.parent / link).resolve()
            if not target.exists():
                broken.append(f"{path}: {link}")
    if broken:
        raise RuntimeError(f"Links rotos: {broken}")


def check_large_files() -> None:
    large: list[str] = []
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        size = path.stat().st_size
        if size > MAX_FILE_SIZE:
            large.append(f"{path} ({size} bytes)")
    if large:
        raise RuntimeError(f"Archivos grandes (>10MB): {large}")


def check_outputs_exist(paths: list[Path]) -> None:
    missing = [str(p) for p in paths if not p.exists()]
    empty = [str(p) for p in paths if p.exists() and p.stat().st_size == 0]
    if missing or empty:
        raise RuntimeError(f"Evidencias faltantes o vacias: missing={missing}, empty={empty}")


def check_evidence_bench_links() -> None:
    text = EVIDENCE_PATH.read_text(encoding="utf-8")
    links = find_links(text)
    missing = REQUIRED_BENCH_LINKS - links
    if missing:
        raise RuntimeError(f"Evidence pack sin links de benchmarks: {sorted(missing)}")


def main() -> None:
    check_readme_sections()
    check_kpi_consistency()

    run_command([sys.executable, "scripts/validate_indra_pack.py"], "validate_indra_pack")
    run_make("test")
    run_make("demo")
    run_make("benchmarks")

    check_outputs_exist([REQUIRED_DEMO_OUTPUT])
    check_outputs_exist(REQUIRED_BENCH_OUTPUTS)
    check_evidence_bench_links()

    check_links_local([README_PATH, *INDRA_DOCS])
    check_large_files()

    print("wow_audit OK")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"wow_audit FAIL: {exc}")
        sys.exit(1)

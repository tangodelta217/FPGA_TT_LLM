from __future__ import annotations

from pathlib import Path
import re
import sys

DOCS = [
    Path("docs/indra/onepager.md"),
    Path("docs/indra/pitchdeck.md"),
    Path("docs/indra/techbrief.md"),
    Path("docs/indra/evidence_pack.md"),
]

REQUIRED_ASSETS = [
    Path("docs/assets/bench_tradeoff.png"),
    Path("docs/assets/kpi_table.md"),
]

EXPECTED_LINKS = {
    "../../README.md",
    "../../scripts/demo_tt_linear.py",
    "../../scripts/run_benchmarks.py",
    "../assets/demo_output.txt",
    "../assets/bench_results.csv",
    "../assets/bench_tradeoff.png",
    "../assets/kpi_table.md",
}


def extract_title(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line.strip()
    raise ValueError(f"No title found in {path}")


def find_links(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    links = set(re.findall(r"\[[^\]]+\]\(([^)]+)\)", text))
    return links


def check_no_todo() -> None:
    for path in DOCS:
        text = path.read_text(encoding="utf-8")
        if "[TODO]" in text:
            raise ValueError(f"[TODO] found in {path}")


def check_titles() -> None:
    titles = [extract_title(doc) for doc in DOCS]
    if len(set(titles)) != 1:
        raise ValueError(f"Titles differ: {titles}")


def check_links() -> None:
    evidence = Path("docs/indra/evidence_pack.md")
    links = find_links(evidence)

    missing_expected = EXPECTED_LINKS - links
    if missing_expected:
        raise ValueError(f"Missing links in evidence_pack.md: {sorted(missing_expected)}")

    for link in links:
        if link.startswith("http") or link.startswith("mailto:") or link.startswith("#"):
            continue
        target = (evidence.parent / link).resolve()
        if not target.exists():
            raise ValueError(f"Broken link in evidence_pack.md: {link}")


def main() -> None:
    missing = [str(doc) for doc in DOCS if not doc.exists()]
    if missing:
        raise FileNotFoundError(f"Missing docs: {missing}")

    missing_assets = [str(asset) for asset in REQUIRED_ASSETS if not asset.exists()]
    if missing_assets:
        raise FileNotFoundError(f"Missing assets: {missing_assets}")

    check_titles()
    check_no_todo()
    check_links()
    print("validate_indra_pack OK")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"validate_indra_pack FAIL: {exc}")
        sys.exit(1)

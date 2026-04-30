#!/usr/bin/env python3
"""Check packaged mcm.skill local references.

This script verifies that Markdown/code references to package-local paths resolve inside
`mcm/`.
It also flags common private or non-packaged path remnants.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple

PACKAGE_PREFIXES = ("references/", "assets/", "scripts/")
PRIVATE_PATTERNS = (
    "docs/evals/regression",
    "docs/evals/cases",
    "docs/evals/test-",
    "docs/runtime",
    "docs/distill",
    "papers/",
    "problems/",
    "/Users/",
)
TEXT_SUFFIXES = {".md", ".py", ".yaml", ".yml", ".txt"}


def iter_text_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if path.is_file() and path.suffix in TEXT_SUFFIXES:
            yield path


def extract_backtick_paths(text: str) -> Iterable[str]:
    for match in re.finditer(r"`([^`]+)`", text):
        value = match.group(1).strip()
        if value.startswith(PACKAGE_PREFIXES):
            yield value


def should_skip_missing(path_text: str, line: str) -> bool:
    if path_text == "scripts/abstract_pool_check.py":
        lowered = line.lower()
        return "if" in lowered or "若存在" in line or "如果" in line or "exists" in lowered
    return False


def check_package(root: Path) -> Tuple[List[str], List[str]]:
    skill_root = root / "mcm"
    missing: List[str] = []
    private: List[str] = []

    for path in iter_text_files(root):
        if path == Path(__file__).resolve():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        rel = path.relative_to(root)

        for pattern in PRIVATE_PATTERNS:
            if pattern in text:
                private.append(f"{rel}: contains private/non-packaged path marker `{pattern}`")

    for path in iter_text_files(skill_root):
        text = path.read_text(encoding="utf-8", errors="ignore")
        rel = path.relative_to(root)

        for line_no, line in enumerate(text.splitlines(), start=1):
            for path_text in extract_backtick_paths(line):
                if should_skip_missing(path_text, line):
                    continue
                target = skill_root / path_text
                if not target.exists():
                    missing.append(f"{rel}:{line_no}: missing `{path_text}`")

    return missing, private


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check mcm.skill package references.")
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Path to the mcm.skill repository root. Defaults to current directory.",
    )
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    missing, private = check_package(root)

    if missing or private:
        print("Package path check failed.")
        for item in missing:
            print(f"[missing] {item}")
        for item in private:
            print(f"[private] {item}")
        return 1

    print("Package path check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

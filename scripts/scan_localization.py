#!/usr/bin/env python3
"""Scan Paradox localization files without modifying them."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


LOCALIZATION_PREFIX_RE = re.compile(
    r"^(?P<indent>\s*)(?P<key>[^:\s][^:]*):(?P<version>\d+)?(?P<space>\s+)"
)
HEADER_RE = re.compile(r"^\s*l_[A-Za-z_]+:\s*(?:#.*)?$")
COMMENT_RE = re.compile(r"^\s*#")
BLANK_RE = re.compile(r"^\s*$")

PROTECTED_PATTERNS = {
    "scripted_loc": re.compile(r"\[[^\]]+\]"),
    "dollar_variable": re.compile(r"\$[^$\s]+\$"),
    "brace_variable": re.compile(r"\{[^{}\s]+\}"),
    "printf": re.compile(r"%[sdif]"),
    "escaped_newline": re.compile(r"\\n"),
    "angle_tag": re.compile(r"<[^<>]+>"),
    "hash_format": re.compile(r"#!|#[A-Za-z_][A-Za-z0-9_]*"),
}


def scan_value(value: str) -> dict[str, list[str]]:
    hits: dict[str, list[str]] = {}
    for name, pattern in PROTECTED_PATTERNS.items():
        matches = pattern.findall(value)
        if matches:
            hits[name] = matches
    return hits


def parse_localization_line(line: str) -> dict[str, str] | None:
    prefix = LOCALIZATION_PREFIX_RE.match(line)
    if not prefix:
        return None

    rest = line[prefix.end() :]
    first_quote = rest.find('"')
    last_quote = rest.rfind('"')
    if first_quote == -1 or last_quote <= first_quote:
        return None

    tail = rest[last_quote + 1 :]
    if tail.strip() and not tail.strip().startswith("#"):
        return None

    return {
        "key": prefix.group("key"),
        "value": rest[first_quote + 1 : last_quote],
    }


def scan_file(path: Path, root: Path) -> dict:
    stats = Counter()
    unparsable: list[dict] = []
    protected: list[dict] = []
    headers: list[dict] = []

    raw = path.read_bytes()
    text = raw.decode("utf-8-sig")
    newline = "crlf" if b"\r\n" in raw else "lf"

    for line_no, line in enumerate(text.splitlines(), 1):
        if BLANK_RE.match(line):
            stats["blank"] += 1
            continue
        if COMMENT_RE.match(line):
            stats["comment"] += 1
            continue
        if HEADER_RE.match(line):
            stats["header"] += 1
            headers.append({"line": line_no, "text": line.strip()})
            continue

        parsed = parse_localization_line(line)
        if parsed:
            stats["localization"] += 1
            value = parsed["value"]
            hits = scan_value(value)
            if hits:
                protected.append(
                    {
                        "line": line_no,
                        "key": parsed["key"],
                        "protected": hits,
                    }
                )
            continue

        stats["unparsable"] += 1
        unparsable.append({"line": line_no, "text": line})

    return {
        "path": str(path.relative_to(root)),
        "bytes": len(raw),
        "newline": newline,
        "stats": dict(stats),
        "headers": headers,
        "unparsable": unparsable,
        "protected": protected,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default="source/english", type=Path)
    parser.add_argument("--report-dir", default="work/reports", type=Path)
    args = parser.parse_args()

    source = args.source.resolve()
    report_dir = args.report_dir.resolve()
    files = sorted(source.rglob("*.yml"))

    report_dir.mkdir(parents=True, exist_ok=True)

    results = [scan_file(path, source) for path in files]
    totals = Counter()
    newline_counts = Counter()
    files_with_unparsable = []
    files_with_protected = []

    for item in results:
        totals.update(item["stats"])
        newline_counts[item["newline"]] += 1
        if item["unparsable"]:
            files_with_unparsable.append(item["path"])
        if item["protected"]:
            files_with_protected.append(item["path"])

    summary = {
        "source": str(source),
        "file_count": len(files),
        "line_totals": dict(totals),
        "newline_counts": dict(newline_counts),
        "files_with_unparsable_count": len(files_with_unparsable),
        "files_with_protected_count": len(files_with_protected),
        "files_with_unparsable": files_with_unparsable,
        "files_with_protected": files_with_protected,
    }

    (report_dir / "localization_scan.json").write_text(
        json.dumps({"summary": summary, "files": results}, ensure_ascii=False, indent=2),
        encoding="utf-8",
        newline="\n",
    )
    (report_dir / "localization_scan_summary.txt").write_text(
        "\n".join(
            [
                f"source: {summary['source']}",
                f"file_count: {summary['file_count']}",
                f"line_totals: {summary['line_totals']}",
                f"newline_counts: {summary['newline_counts']}",
                f"files_with_unparsable_count: {summary['files_with_unparsable_count']}",
                f"files_with_protected_count: {summary['files_with_protected_count']}",
            ]
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if not files_with_unparsable else 1


if __name__ == "__main__":
    raise SystemExit(main())

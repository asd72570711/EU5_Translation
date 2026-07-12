#!/usr/bin/env python3
"""Validate translated Paradox localization files against their source files."""

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
LANGUAGE_FOLDER_NAMES = {"english", "simp_chinese"}

PROTECTED_PATTERNS = {
    "scripted_loc": re.compile(r"\[[^\]]+\]"),
    "at_icon": re.compile(r"@[A-Za-z_][A-Za-z0-9_]*!"),
    "steam_result": re.compile(r"k_EResult[A-Za-z0-9_]+"),
    "dollar_variable": re.compile(r"\$[^$\s]+\$"),
    "brace_variable": re.compile(r"\{[^{}\s]+\}"),
    "printf": re.compile(r"%[sdif]"),
    "escaped_newline": re.compile(r"\\n"),
    "angle_tag": re.compile(r"<[^<>]+>"),
    "hash_format": re.compile(r"#!|#[A-Za-z_][A-Za-z0-9_]*"),
}


def parse_localization_line(line: str) -> dict[str, str] | None:
    if line.lstrip().startswith("#"):
        return None

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


def protected_tokens(value: str) -> dict[str, list[str]]:
    hits: dict[str, list[str]] = {}
    for name, pattern in PROTECTED_PATTERNS.items():
        matches = pattern.findall(value)
        if matches:
            hits[name] = matches
    return hits


def protected_token_counts(tokens: dict[str, list[str]]) -> dict[str, dict[str, int]]:
    return {
        name: dict(sorted(Counter(matches).items()))
        for name, matches in sorted(tokens.items())
    }


def read_localization(path: Path) -> dict:
    raw = path.read_bytes()
    text = raw.decode("utf-8-sig")
    lines = text.splitlines()
    entries: list[dict] = []
    headers: list[str] = []

    for line_no, line in enumerate(lines, 1):
        if HEADER_RE.match(line):
            headers.append(line.strip())

        parsed = parse_localization_line(line)
        if not parsed:
            continue

        entries.append(
            {
                "line": line_no,
                "key": parsed["key"],
                "protected": protected_tokens(parsed["value"]),
            }
        )

    return {
        "path": str(path),
        "line_count": len(lines),
        "headers": headers,
        "entries": entries,
    }


def expected_headers(headers: list[str], target_language: str) -> list[str]:
    expected: list[str] = []
    for header in headers:
        expected.append(re.sub(r"l_[A-Za-z_]+:", f"l_{target_language}:", header, count=1))
    return expected


def validate(source: dict, output: dict, target_language: str) -> dict:
    errors: list[dict] = []
    source_keys = [entry["key"] for entry in source["entries"]]
    output_keys = [entry["key"] for entry in output["entries"]]

    if source_keys != output_keys:
        errors.append(
            {
                "type": "key_sequence_mismatch",
                "source_key_count": len(source_keys),
                "output_key_count": len(output_keys),
            }
        )

    for index, (source_entry, output_entry) in enumerate(
        zip(source["entries"], output["entries"]), 1
    ):
        if source_entry["key"] != output_entry["key"]:
            errors.append(
                {
                    "type": "key_mismatch",
                    "index": index,
                    "source": source_entry,
                    "output": output_entry,
                }
            )
            continue

        source_tokens = protected_token_counts(source_entry["protected"])
        output_tokens = protected_token_counts(output_entry["protected"])
        if source_tokens != output_tokens:
            errors.append(
                {
                    "type": "protected_token_mismatch",
                    "key": source_entry["key"],
                    "source_line": source_entry["line"],
                    "output_line": output_entry["line"],
                    "source": source_tokens,
                    "output": output_tokens,
                }
            )

    return {
        "source": source["path"],
        "output": output["path"],
        "source_entries": len(source["entries"]),
        "output_entries": len(output["entries"]),
        "headers_match": expected_headers(source["headers"], target_language) == output["headers"],
        "expected_headers": expected_headers(source["headers"], target_language),
        "output_headers": output["headers"],
        "errors": errors,
    }


def target_relative_path(rel_path: Path, target_language: str) -> Path:
    parts = [
        target_language if part in LANGUAGE_FOLDER_NAMES else part
        for part in rel_path.parts
    ]
    path = Path(*parts)
    suffix = "_l_english.yml"
    if path.name.endswith(suffix):
        path = path.with_name(path.name[: -len(suffix)] + f"_l_{target_language}.yml")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", default="source/english", type=Path)
    parser.add_argument("--output-root", default="output/traditional_chinese", type=Path)
    parser.add_argument("--file", required=True, help="Path relative to --source-root")
    parser.add_argument("--target-language", default="simp_chinese")
    args = parser.parse_args()

    source_path = (args.source_root / args.file).resolve()
    output_path = (args.output_root / target_relative_path(Path(args.file), args.target_language)).resolve()
    if not source_path.is_file():
        raise FileNotFoundError(source_path)
    if not output_path.is_file():
        raise FileNotFoundError(output_path)

    result = validate(read_localization(source_path), read_localization(output_path), args.target_language)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not result["errors"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

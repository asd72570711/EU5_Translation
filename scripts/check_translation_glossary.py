#!/usr/bin/env python3
"""Check that glossary terms found in source values use their glossary translations."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ENTRY_RE = re.compile(r'^\s*([^#\s][^:]*):\s*"(.*)"\s*(?:#.*)?$')


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def source_entries(path: Path) -> dict[str, str]:
    entries: dict[str, str] = {}
    for line in read_text(path).splitlines():
        match = ENTRY_RE.match(line)
        if match:
            entries[match.group(1).strip()] = match.group(2)
    return entries


def glossary_entries(path: Path) -> dict[str, str]:
    entries: dict[str, str] = {}
    current_term: str | None = None
    alias_term: str | None = None
    alias_translation: str | None = None
    alias_names: list[str] = []
    in_aliases = False

    def flush_alias() -> None:
        if alias_term and alias_translation:
            entries[alias_term] = alias_translation
            for alias in alias_names:
                entries[alias] = alias_translation

    for line in read_text(path).splitlines():
        if line == "aliases:":
            flush_alias()
            in_aliases = True
            alias_term = None
            alias_translation = None
            alias_names = []
            continue
        if in_aliases and line and not line.startswith(" "):
            flush_alias()
            in_aliases = False
            alias_term = None
            alias_translation = None
            alias_names = []

        if in_aliases:
            alias = re.match(r"^  (?! )([^:#][^:]+):\s*$", line)
            if alias:
                flush_alias()
                alias_term = alias.group(1).strip()
                alias_translation = None
                alias_names = []
                continue
            zh = re.match(r'^    zh:\s*"([^"]*)"', line)
            if zh and alias_term:
                alias_translation = zh.group(1)
                continue
            also = re.match(r"^      -\s+(.+?)\s*$", line)
            if also and alias_term:
                alias_names.append(also.group(1).strip())
            continue

        scalar = re.match(r'^  (?! )([^:#][^:]+):\s*"([^"]*)"', line)
        if scalar:
            entries[scalar.group(1).strip()] = scalar.group(2)
            current_term = None
            continue

        block = re.match(r"^  (?! )([^:#][^:]+):\s*$", line)
        if block:
            current_term = block.group(1).strip()
            continue

        if current_term:
            default = re.match(r'^    (?:default|zh):\s*"([^"]*)"', line)
            if default and current_term not in entries:
                entries[current_term] = default.group(1)
    flush_alias()
    return entries


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", required=True, type=Path)
    parser.add_argument("--translations", required=True, type=Path)
    parser.add_argument("--glossary", default="translation_glossary.yml", type=Path)
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    source = source_entries(args.file)
    translations = json.loads(args.translations.read_text(encoding="utf-8"))
    glossary = glossary_entries(args.glossary)
    mismatches: list[dict[str, str]] = []

    for key, source_value in source.items():
        translated_value = translations.get(key)
        if not isinstance(translated_value, str):
            continue
        if key.endswith("_EFFECTS") and translated_value in {"$EFFECT$", "$EFFECT$"}:
            continue
        for term, expected in glossary.items():
            if term == "Reformation" and re.search(
                r"Reformation of the (?:Infantry|Cavalry|Thema Headquarters|Galley Fleet|Merchant Fleet|School of Admirals|[^\"]+ Military)",
                source_value,
            ):
                continue
            term_pattern = r"(?<![A-Za-z])" + re.escape(term) + r"(?![A-Za-z])"
            nested_in_longer = any(
                longer != term
                and len(longer) > len(term)
                and term in longer
                and re.search(
                    r"(?<![A-Za-z])" + re.escape(longer) + r"(?![A-Za-z])",
                    source_value,
                )
                for longer in glossary
            )
            if nested_in_longer:
                continue
            if " " not in term:
                capitalized_phrase = (
                    r"(?<![A-Za-z])"
                    + re.escape(term)
                    + r"\s+[A-Z\u00C0-\u00DE][A-Za-z\u00C0-\u024F'’-]*"
                )
                if re.search(capitalized_phrase, source_value):
                    continue
            if re.search(term_pattern, source_value) and expected and expected not in translated_value:
                mismatches.append(
                    {
                        "key": key,
                        "term": term,
                        "expected": expected,
                        "translation": translated_value,
                    }
                )

    print(json.dumps({"mismatches": mismatches}, ensure_ascii=False, indent=2))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())

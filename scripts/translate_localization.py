#!/usr/bin/env python3
"""Apply approved translations to one Paradox localization file."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


LOCALIZATION_PREFIX_RE = re.compile(
    r"^(?P<indent>\s*)(?P<key>[^:\s][^:]*):(?P<version>\d+)?(?P<space>\s+)"
)
HEADER_RE = re.compile(r"^(?P<indent>\s*)l_[A-Za-z_]+:(?P<tail>\s*(?:#.*)?)$")
LANGUAGE_FOLDER_NAMES = {"english", "simp_chinese"}


def parse_localization_line(line: str) -> dict[str, int | str] | None:
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
        "value_start": prefix.end() + first_quote + 1,
        "value_end": prefix.end() + last_quote,
    }


def load_translations(path: Path) -> dict[str, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("translations JSON must be an object mapping keys to strings")

    translations: dict[str, str] = {}
    for key, value in data.items():
        if not isinstance(key, str) or not isinstance(value, str):
            raise ValueError("translations JSON must map string keys to string values")
        if "\n" in value or "\r" in value:
            raise ValueError(
                f"translation for {key!r} contains a real newline; use literal \\\\n"
            )
        translations[key] = value
    return translations


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


def translate_lines(
    lines: list[str],
    translations: dict[str, str],
    target_language: str,
) -> tuple[list[str], dict]:
    output: list[str] = []
    used_keys: set[str] = set()
    stats = {
        "localization_lines": 0,
        "translated_lines": 0,
        "untranslated_keys": [],
    }

    for line in lines:
        header = HEADER_RE.match(line)
        if header:
            output.append(f"{header.group('indent')}l_{target_language}:{header.group('tail')}")
            continue

        parsed = parse_localization_line(line)
        if not parsed:
            output.append(line)
            continue

        stats["localization_lines"] += 1
        key = str(parsed["key"])
        if key not in translations:
            stats["untranslated_keys"].append(key)
            output.append(line)
            continue

        start = int(parsed["value_start"])
        end = int(parsed["value_end"])
        output.append(line[:start] + translations[key] + line[end:])
        used_keys.add(key)
        stats["translated_lines"] += 1

    stats["unused_translation_keys"] = sorted(set(translations) - used_keys)
    return output, stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", default="source/english", type=Path)
    parser.add_argument("--output-root", default="output/traditional_chinese", type=Path)
    parser.add_argument("--file", required=True, help="Path relative to --source-root")
    parser.add_argument("--translations", required=True, type=Path)
    parser.add_argument("--glossary", default="translation_glossary.yml", type=Path)
    parser.add_argument(
        "--check-glossary",
        action="store_true",
        help="Check glossary consistency before producing output",
    )
    parser.add_argument(
        "--check-style",
        action="store_true",
        help="Check translation style before producing output",
    )
    parser.add_argument("--target-language", default="simp_chinese")
    parser.add_argument("--write", action="store_true", help="Write output file")
    args = parser.parse_args()

    source_root = args.source_root.resolve()
    output_root = args.output_root.resolve()
    rel_path = Path(args.file)
    source_path = (source_root / rel_path).resolve()
    output_rel_path = target_relative_path(rel_path, args.target_language)
    output_path = (output_root / output_rel_path).resolve()

    if not source_path.is_file():
        raise FileNotFoundError(source_path)
    if not str(source_path).startswith(str(source_root)):
        raise ValueError("source file must stay under source root")
    if not str(output_path).startswith(str(output_root)):
        raise ValueError("output file must stay under output root")

    raw = source_path.read_bytes()
    newline = "\r\n" if b"\r\n" in raw else "\n"
    text = raw.decode("utf-8-sig")
    lines = text.splitlines()
    translations = load_translations(args.translations)

    if args.check_glossary:
        checker = Path(__file__).with_name("check_translation_glossary.py")
        check = subprocess.run(
            [
                sys.executable,
                str(checker),
                "--file",
                str(source_path),
                "--translations",
                str(args.translations.resolve()),
                "--glossary",
                str(args.glossary.resolve()),
            ],
            check=False,
        )
        if check.returncode:
            raise ValueError("glossary consistency check failed; output was not written")

    if args.check_style:
        checker = Path(__file__).with_name("check_translation_style.py")
        check = subprocess.run(
            [sys.executable, str(checker), "--translations", str(args.translations.resolve())],
            check=False,
        )
        if check.returncode:
            raise ValueError("translation style check failed; output was not written")

    translated, stats = translate_lines(lines, translations, args.target_language)
    stats["output_file"] = str(output_rel_path)

    print(json.dumps(stats, ensure_ascii=False, indent=2))

    if args.write:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(newline.join(translated) + newline, encoding="utf-8", newline="")
        print(f"wrote: {output_path}")
    else:
        print("dry-run only; pass --write to write output")

    return 0 if not stats["unused_translation_keys"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

import re
import sys
from collections import defaultdict
from pathlib import Path


PATH = Path("translation_glossary.yml")
SECTION_NAMES = {"fixed", "game_terms", "aliases", "contextual"}


def quoted_value(line: str) -> str | None:
    match = re.search(r':\s*"([^"]*)"', line)
    return match.group(1) if match else None


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    lines = PATH.read_text(encoding="utf-8-sig").splitlines()
    section = None
    scalar: dict[str, list[tuple[str, str]]] = defaultdict(list)
    aliases: list[tuple[str, str, list[str]]] = []
    contextual: dict[str, str] = {}
    alias_term = None
    alias_zh = None
    alias_also: list[str] = []
    contextual_term = None

    def flush_alias() -> None:
        nonlocal alias_term, alias_zh, alias_also
        if alias_term and alias_zh:
            aliases.append((alias_term, alias_zh, alias_also))
        alias_term = None
        alias_zh = None
        alias_also = []

    for line in lines:
        if line and not line.startswith(" ") and line.rstrip(":") in SECTION_NAMES:
            flush_alias()
            section = line.rstrip(":")
            contextual_term = None
            continue
        if section == "aliases":
            match = re.match(r"^  (?! )([^:#][^:]*):\s*$", line)
            if match:
                flush_alias()
                alias_term = match.group(1).strip()
                continue
            match = re.match(r'^    zh:\s*"([^"]*)"', line)
            if match:
                alias_zh = match.group(1)
                continue
            match = re.match(r"^      -\s+(.+?)\s*$", line)
            if match and alias_term:
                alias_also.append(match.group(1).strip())
                continue
        elif section in {"fixed", "game_terms"}:
            match = re.match(r'^  (?! )([^:#][^:]*):\s*"([^"]*)"', line)
            if match:
                scalar[section].append((match.group(1).strip(), match.group(2)))
        elif section == "contextual":
            match = re.match(r"^  (?! )([^:#][^:]*):", line)
            if match:
                contextual_term = match.group(1).strip()
                continue
            if contextual_term:
                value = quoted_value(line)
                if line.startswith("    default:") and value is not None:
                    contextual[contextual_term] = value
    flush_alias()

    print("DUPLICATE FIXED TRANSLATIONS")
    groups: dict[str, list[str]] = defaultdict(list)
    for term, value in scalar["fixed"]:
        groups[value].append(term)
    for value, terms in sorted(groups.items(), key=lambda item: item[0]):
        if len(terms) > 1:
            print(f"{value}\t" + " | ".join(terms))

    print("\nDUPLICATE KEYS")
    all_keys: dict[str, list[str]] = defaultdict(list)
    for name in ("fixed", "game_terms"):
        for term, _ in scalar[name]:
            all_keys[term].append(name)
    for term, _, _ in aliases:
        all_keys[term].append("aliases")
    for term in contextual:
        all_keys[term].append("contextual")
    for term, sections in sorted(all_keys.items(), key=lambda item: item[0].casefold()):
        if len(sections) > 1:
            print(f"{term}\t" + " | ".join(sections))

    print("\nORDER VIOLATIONS")
    for name in ("fixed", "game_terms"):
        terms = [term for term, _ in scalar[name]]
        expected = sorted(terms, key=str.casefold)
        if terms != expected:
            index = next(i for i, pair in enumerate(zip(terms, expected)) if pair[0] != pair[1])
            print(f"{name}: {len(terms)} entries; first mismatch at index {index}")
            print("  actual:", " | ".join(terms[max(0, index - 2):index + 3]))
            print("  expected:", " | ".join(expected[max(0, index - 2):index + 3]))
    terms = [term for term, _, _ in aliases]
    expected = sorted(terms, key=str.casefold)
    if terms != expected:
        index = next(i for i, pair in enumerate(zip(terms, expected)) if pair[0] != pair[1])
        print("aliases: first mismatch at index", index)
        print("  actual:", " | ".join(terms[max(0, index - 2):index + 3]))
        print("  expected:", " | ".join(expected[max(0, index - 2):index + 3]))
    terms = list(contextual)
    expected = sorted(terms, key=str.casefold)
    if terms != expected:
        index = next(i for i, pair in enumerate(zip(terms, expected)) if pair[0] != pair[1])
        print("contextual: first mismatch at index", index)
        print("  actual:", " | ".join(terms[max(0, index - 2):index + 3]))
        print("  expected:", " | ".join(expected[max(0, index - 2):index + 3]))


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


LATIN_UPPER = r"A-Z\u00C0-\u00DE"
LATIN_LETTER = r"A-Za-z\u00C0-\u024F"
APOSTROPHE = r"'\u2019"
QUOTE_CHARS = "\"'\u201c\u201d"

ENTRY_RE = re.compile(r'^\s*([^#\s][^:]*):\s*"(.*)"\s*(?:#.*)?$')
PROTECTED_RE = re.compile(
    r"\$[^$]+\$|\[[^\]]+\]|#\w+|#!|\\n|@[A-Za-z0-9_]+!|<[^>]+>"
)
WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9'._-]*")
TITLE_CASE_RE = re.compile(
    rf"\b[{LATIN_UPPER}][{LATIN_LETTER}{APOSTROPHE}.-]+"
    rf"(?:\s+(?:of|de|del|da|di|du|von|van|the|and|la|le|des|"
    rf"d[{APOSTROPHE}][{LATIN_UPPER}][{LATIN_LETTER}{APOSTROPHE}.-]+|"
    rf"d[{APOSTROPHE}]|"
    r"I|II|III|IV|V|VI|VII|VIII|IX|X|XI|XII|"
    rf"[{LATIN_UPPER}][{LATIN_LETTER}{APOSTROPHE}.-]+))*\b"
)

IGNORE_TERMS = {
    "A",
    "Air",
    "All",
    "And",
    "As",
    "Can",
    "Christ",
    "Christian",
    "Christianity",
    "Christendom",
    "Church",
    "Earth",
    "England",
    "English",
    "For",
    "French",
    "German",
    "God",
    "Great Spirit",
    "Greeks",
    "Here",
    "If",
    "In",
    "Italian",
    "King",
    "Latins",
    "Lord",
    "Man",
    "No",
    "Nothing",
    "On",
    "Or",
    "Our",
    "Papal",
    "Pope",
    "Rather",
    "Spanish",
    "Spaniard",
    "The",
    "These",
    "Those",
    "Turkish",
    "What",
}

TRAILING_CONNECTORS = {
    "and",
    "da",
    "de",
    "del",
    "des",
    "di",
    "du",
    "la",
    "le",
    "of",
    "the",
    "van",
    "von",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def parse_entries(path: Path) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    for line in read_text(path).splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        match = ENTRY_RE.match(line)
        if match:
            entries.append((match.group(1).strip(), match.group(2)))
    return entries


def glossary_entries(glossary_path: Path) -> dict[str, str]:
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

    for line in read_text(glossary_path).splitlines():
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


def candidates(entries: list[tuple[str, str]]) -> dict[str, set[str]]:
    found: dict[str, set[str]] = {}
    for key, value in entries:
        clean = PROTECTED_RE.sub(lambda match: " " * len(match.group(0)), value)
        for match in TITLE_CASE_RE.finditer(clean):
            term = normalize_candidate(match.group(0))
            if not term:
                continue
            if is_sentence_initial_single_word(clean, match.start(), term):
                continue
            if is_sentence_fragment(term):
                continue
            found.setdefault(term, set()).add(key)
    return found


def normalize_candidate(term: str) -> str | None:
    term = term.strip(f" ,.;:!?{QUOTE_CHARS}()[]")
    parts = term.split()
    while parts and parts[-1].lower() in TRAILING_CONNECTORS:
        parts.pop()
    term = " ".join(parts)
    if len(term) < 3 or term in IGNORE_TERMS:
        return None
    return term


def is_sentence_fragment(term: str) -> bool:
    return bool(re.search(r"\.\s+[A-Z]", term))


def is_sentence_initial_single_word(clean_value: str, start: int, term: str) -> bool:
    term_words = words(term)
    is_single_word = len(term_words) <= 1 and " " not in term
    if not is_single_word:
        return False

    stripped_value = clean_value.strip(f" \t{QUOTE_CHARS}")
    if stripped_value == term:
        return False

    prefix = clean_value[:start].rstrip()
    if not prefix:
        return True

    last = prefix[-1]
    if last in f"{QUOTE_CHARS}([{{":
        return True
    if last in ".!?":
        return True

    return False


def words(term: str) -> set[str]:
    ignored = {
        "a",
        "an",
        "and",
        "by",
        "de",
        "del",
        "of",
        "the",
        "to",
        "van",
        "von",
        "i",
        "ii",
        "iii",
        "iv",
        "v",
        "vi",
        "vii",
        "viii",
        "ix",
        "x",
        "xi",
        "xii",
    }
    return {
        word.lower()
        for word in WORD_RE.findall(term)
        if word.lower() not in ignored and len(word) > 1
    }


def glossary_refs(term: str, glossary: dict[str, str], limit: int = 12) -> list[dict[str, str]]:
    term_lower = term.lower()
    term_words = words(term)
    refs: list[tuple[int, str, str]] = []
    for known_term, translation in glossary.items():
        known_lower = known_term.lower()
        known_words = words(known_term)
        score = 0
        if known_lower == term_lower:
            score += 100
        elif known_lower in term_lower or term_lower in known_lower:
            score += 50
        overlap = term_words & known_words
        if overlap:
            score += 10 * len(overlap)
        if score:
            refs.append((score, known_term, translation))

    refs.sort(key=lambda item: (-item[0], item[1].lower()))
    return [
        {"term": known_term, "translation": translation}
        for _, known_term, translation in refs[:limit]
    ]


def guess_category(term: str) -> str:
    lowered = term.lower()
    if any(word in lowered for word in ("battle", "siege", "war")):
        return "event"
    if any(
        word in lowered
        for word in ("declaration", "theses", "essay", "discourse", "books", "histories")
    ):
        return "work_title"
    if any(word in lowered for word in ("order", "commonwealth", "church")):
        return "organization"
    if any(
        word in lowered
        for word in ("king", "emperor", "pope", "marquis", "archbishop", "admiral", "captain")
    ):
        return "title_or_role"
    if re.search(r"\b(of|de|del|da|di|du|von|van|d['\u2019])", term):
        return "person_or_place"
    if re.search(r"\b[IVX]+\b", term):
        return "person"
    return "unknown"


def existing_review_items(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {
        item["term"]: item
        for item in data.get("items", [])
        if isinstance(item, dict) and item.get("term")
    }


def build_review_item(
    term: str,
    keys: list[str],
    glossary: dict[str, str],
    existing: dict[str, Any] | None,
) -> dict[str, Any]:
    item = {
        "term": term,
        "translation": "",
        "status": "todo",
        "category": guess_category(term),
        "keys": keys,
        "note": "",
        "glossary_refs": glossary_refs(term, glossary),
    }
    if existing:
        for field in ("translation", "category", "status", "note"):
            if field in existing:
                item[field] = existing[field]
        if "keys" in existing:
            item["keys"] = sorted(set(existing["keys"]) | set(keys))
    return item


def write_review_json(
    output_path: Path,
    source_file: list[str],
    rows: list[tuple[str, str, list[str]]],
    glossary: dict[str, str],
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    existing_items = existing_review_items(output_path)
    review_items = [
        build_review_item(term, keys, glossary, existing_items.get(term))
        for status, term, keys in rows
        if status == "review"
    ]
    review = {
        "source_file": source_file,
        "status": "todo",
        "instructions": (
            "Status values: todo=fill translation manually, "
            "ai=let Codex suggest translation in review.json, "
            "cont=have Codex propose a contextual glossary rule from source contexts, "
            "skip=ignore. glossary_refs are references only."
        ),
        "items": review_items,
    }
    output_path.write_text(json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, action="append")
    parser.add_argument("--source-root", default="source/english")
    parser.add_argument("--glossary", default="translation_glossary.yml")
    parser.add_argument("--review-only", action="store_true")
    parser.add_argument("--write-review", action="store_true")
    parser.add_argument("--review-output", default="work/glossary_review/review.json")
    args = parser.parse_args()

    sys.stdout.reconfigure(encoding="utf-8")

    glossary_path = Path(args.glossary)
    glossary = glossary_entries(glossary_path)
    known = set(glossary)
    candidate_terms: dict[str, list[str]] = {}
    scanned_files: list[str] = []
    for source_file in args.file:
        source_path = Path(args.source_root) / source_file
        paths = sorted(source_path.rglob("*.yml")) if source_path.is_dir() else [source_path]
        for path in paths:
            relative = path.relative_to(Path(args.source_root)).as_posix()
            scanned_files.append(relative)
            for term, keys in candidates(parse_entries(path)).items():
                candidate_terms.setdefault(term, []).extend(keys)

    rows = []
    for term, keys in sorted(candidate_terms.items(), key=lambda x: x[0].lower()):
        keys = sorted(set(keys))
        status = "known" if term in known else "review"
        if args.review_only and status == "known":
            continue
        rows.append((status, term, sorted(keys)))

    if args.write_review:
        review_rows = [row for row in rows if row[0] == "review"]
        write_review_json(Path(args.review_output), scanned_files, review_rows, glossary)
        print(f"wrote: {args.review_output}")
        print(f"review_items: {len(review_rows)}")
        return 0

    print(f"files: {', '.join(scanned_files)}")
    print(f"candidates: {len(rows)}")
    print("status\tterm\tkeys\tglossary_refs")
    for status, term, keys in rows:
        refs = glossary_refs(term, glossary)
        ref_text = "; ".join(f"{ref['term']}={ref['translation']}" for ref in refs[:5])
        print(f"{status}\t{term}\t{', '.join(keys)}\t{ref_text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

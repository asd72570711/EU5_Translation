from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any


DEFAULT_REVIEW = Path("work/glossary_review/review.json")
DEFAULT_GLOSSARY = Path("translation_glossary.yml")
DEFAULT_DROP_TERMS = Path("glossary_drop_terms.yml")

WHEN_CONTEXTUAL = "\u4f9d\u5b8c\u6574\u4e0a\u4e0b\u6587\u5224\u65b7\u8a72\u8b6f\u540d\u7684\u9069\u7528\u8a9e\u5883"
CONTROL_VALUES = {"ai", "cont", "drop", "skip"}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def normalized_drop_term(term: str) -> str:
    normalized = unicodedata.normalize("NFKD", term)
    normalized = "".join(
        char for char in normalized if not unicodedata.combining(char)
    )
    normalized = normalized.replace("\u2019", "'").replace("`", "'")
    normalized = re.sub(r"['\u2019]s\b", "", normalized, flags=re.IGNORECASE)
    return re.sub(r"[^A-Za-z0-9]+", " ", normalized).strip().casefold()


def load_drop_terms(path: Path) -> tuple[set[str], str]:
    if not path.exists():
        return set(), ""

    text = read_text(path)
    terms: set[str] = set()
    in_drop_terms = False
    for line in text.splitlines():
        if line.strip() == "drop_terms:":
            in_drop_terms = True
            continue
        if in_drop_terms and line and not line.startswith((" ", "\t", "#")):
            in_drop_terms = False
        if not in_drop_terms:
            continue
        match = re.match(
            r'^\s*-\s*(?:"([^"]*)"|\'([^\']*)\'|([^#]+?))\s*(?:#.*)?$',
            line,
        )
        if match:
            value = next(
                (part for part in match.groups() if part is not None), ""
            )
            normalized = normalized_drop_term(value.strip())
            if normalized:
                terms.add(normalized)
    return terms, text


def add_drop_terms(path: Path, terms: list[str]) -> dict[str, int]:
    existing, text = load_drop_terms(path)
    additions: list[str] = []
    for term in terms:
        normalized = normalized_drop_term(term)
        if normalized and normalized not in existing:
            existing.add(normalized)
            additions.append(term)

    if not additions:
        return {"drop_added": 0}

    if not text.strip():
        output = "# User-confirmed terms that should not be added to review.\ndrop_terms:\n"
    elif "drop_terms:" not in text.splitlines():
        output = text.rstrip("\r\n") + "\n\ndrop_terms:\n"
    else:
        output = text if text.endswith(("\n", "\r")) else text + "\n"
    output += "".join(f"  - {yaml_quote(term)}\n" for term in additions)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(output, encoding="utf-8")
    return {"drop_added": len(additions)}


def yaml_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def glossary_terms(text: str) -> set[str]:
    terms: set[str] = set()
    alias_term: str | None = None
    alias_names: list[str] = []
    in_aliases = False

    def flush_alias() -> None:
        if alias_term:
            terms.add(alias_term)
            terms.update(alias_names)

    for line in text.splitlines():
        if line == "aliases:":
            flush_alias()
            in_aliases = True
            alias_term = None
            alias_names = []
            continue
        if in_aliases and line and not line.startswith(" "):
            flush_alias()
            in_aliases = False
            alias_term = None
            alias_names = []

        if in_aliases:
            alias = re.match(r"^  (?! )([^:#][^:]+):\s*$", line)
            if alias:
                flush_alias()
                alias_term = alias.group(1).strip()
                alias_names = []
                continue
            also = re.match(r"^      -\s+(.+?)\s*$", line)
            if also and alias_term:
                alias_names.append(also.group(1).strip())
            continue

        match = re.match(r"^  (?! )([^:#][^:]+):", line)
        if match:
            terms.add(match.group(1).strip())
    flush_alias()
    return terms


def importable_items(
    review: dict[str, Any],
    resolved_only: bool,
    include_cont: bool,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    items = []
    contextual_items = []
    for item in review.get("items", []):
        status = item.get("status")
        translation = item.get("translation", "").strip()
        if status == "drop":
            continue
        if status == "skip":
            continue
        if status == "cont":
            if not include_cont:
                continue
            if not translation:
                if resolved_only:
                    continue
                raise ValueError(f"Missing translation for {item.get('term')}")
            # A resolved cont is explicitly a contextual candidate. Never let
            # an unlisted cont silently fall back to fixed.
            contextual_items.append(item)
            continue
        if status not in {"todo", "ai"}:
            if resolved_only:
                # Keep malformed or user-entered statuses for manual repair.
                continue
            raise ValueError(f"Unsupported status for {item.get('term')}: {status}")
        if status == "todo" and translation.lower() in CONTROL_VALUES:
            raise ValueError(
                f"Control value used as translation for {item.get('term')}; use status instead"
            )
        if not translation:
            if resolved_only:
                continue
            raise ValueError(f"Missing translation for {item.get('term')}")
        if resolved_only and status not in {"todo", "ai"}:
            continue
        items.append(item)
    return items, contextual_items


def drop_items(review: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        item
        for item in review.get("items", [])
        if item.get("status") == "drop" and item.get("term")
    ]


def remove_processed_items(
    review: dict[str, Any],
    imported_terms: set[str],
    remove_skip: bool,
) -> dict[str, int]:
    retained = []
    removed_skip = 0
    removed_imported = 0
    removed_drop = 0
    for item in review.get("items", []):
        if remove_skip and item.get("status") == "skip":
            removed_skip += 1
            continue
        if item.get("status") == "drop":
            removed_drop += 1
            continue
        if item.get("term") in imported_terms and item.get("status") in {"todo", "ai", "cont"}:
            removed_imported += 1
            continue
        retained.append(item)
    review["items"] = retained
    return {
        "removed_skip": removed_skip,
        "removed_imported": removed_imported,
        "removed_drop": removed_drop,
    }


def yaml_inline_comment(note: str) -> str:
    return " / ".join(line.strip() for line in note.splitlines() if line.strip())


def split_contextual_translations(
    translation: str, split_senses: bool
) -> list[str]:
    if not split_senses:
        return [translation.strip()] if translation.strip() else []
    values = re.split(r"\s*[\u3001\uff0c,;]\s*", translation.strip())
    result = []
    for value in values:
        value = value.strip()
        if value and value not in result:
            result.append(value)
    return result


def contextual_block(
    term: str, translation: str, note: str, split_senses: bool = False
) -> list[str]:
    heading = f"  {term}:"
    if note:
        heading += f"  # {yaml_inline_comment(note)}"
    provided = split_contextual_translations(translation, split_senses)
    senses = [(value, WHEN_CONTEXTUAL) for value in provided]
    if not senses and translation.strip():
        senses = [(translation.strip(), WHEN_CONTEXTUAL)]
    if not senses:
        raise ValueError(f"Missing contextual translation for {term}")
    default = senses[0][0]
    lines = [heading, f"    default: {yaml_quote(default)}", "    senses:"]
    for zh, when in senses:
        lines.extend([f"      - zh: {yaml_quote(zh)}", f"        when: {yaml_quote(when)}"])
    return lines

def apply_import(
    glossary_text: str,
    items: list[dict[str, Any]],
    contextual_items: list[dict[str, Any]],
) -> tuple[str, dict[str, Any], set[str]]:
    existing = glossary_terms(glossary_text)
    fixed_items: list[tuple[str, str, str]] = []
    contextual_lines: list[str] = []
    imported_terms: set[str] = set()
    skipped_existing = 0

    for item in contextual_items:
        term = item["term"]
        if term in existing:
            skipped_existing += 1
            imported_terms.add(term)
            continue
        contextual_lines.extend(
            contextual_block(
                term,
                item["translation"],
                item.get("note", "").strip(),
                split_senses=True,
            )
        )
        existing.add(term)
        imported_terms.add(term)

    for item in items:
        term = item["term"]
        # Copy the confirmed review value verbatim; semantic changes belong to AI.
        translation = item["translation"]
        if term in existing:
            skipped_existing += 1
            imported_terms.add(term)
            continue
        fixed_items.append((term, translation, item.get("note", "").strip()))
        existing.add(term)
        imported_terms.add(term)

    lines = glossary_text.splitlines()
    if fixed_items:
        fixed_lines: list[str] = []
        # Preserve review order; glossary sorting is an explicit separate operation.
        for term, translation, note in fixed_items:
            line = f"  {term}: {yaml_quote(translation)}"
            if note:
                line += f"  # {yaml_inline_comment(note)}"
            fixed_lines.append(line)
        aliases_index = next(i for i, line in enumerate(lines) if line.startswith("aliases:"))
        lines[aliases_index:aliases_index] = fixed_lines + [""]

    if contextual_lines:
        reference_index = next(
            i for i, line in enumerate(lines) if line == "reference_terms:"
        )
        lines[reference_index:reference_index] = [""] + contextual_lines

    stats = {
        "fixed_added": len(fixed_items),
        "contextual_added": sum(1 for line in contextual_lines if re.match(r"^  [^ ].*:$", line)),
        "skipped_existing": skipped_existing,
    }
    return "\n".join(lines) + "\n", stats, imported_terms


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review", default=str(DEFAULT_REVIEW))
    parser.add_argument("--glossary", default=str(DEFAULT_GLOSSARY))
    parser.add_argument("--drop-terms", default=str(DEFAULT_DROP_TERMS))
    parser.add_argument(
        "--resolved-only",
        action="store_true",
        help="Import filled todo items and remove them plus skip items from the review",
    )
    parser.add_argument(
        "--include-cont",
        action="store_true",
        help="Import cont items only after AI has completed contextual judgment",
    )
    parser.add_argument(
        "--keep-review",
        action="store_true",
        help="Write glossary changes without removing processed review items",
    )
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    sys.stdout.reconfigure(encoding="utf-8")

    review_path = Path(args.review)
    glossary_path = Path(args.glossary)
    drop_path = Path(args.drop_terms)
    review = json.loads(review_path.read_text(encoding="utf-8"))
    glossary_text = read_text(glossary_path)
    pending_drop_items = drop_items(review)
    items, contextual_items = importable_items(
        review,
        args.resolved_only,
        args.include_cont,
    )
    new_text, stats, imported_terms = apply_import(
        glossary_text, items, contextual_items
    )

    stats["importable_items"] = len(items)
    stats["pending_contextual"] = len(contextual_items)
    stats["contextual_terms"] = [item.get("term") for item in contextual_items]
    stats["drop_items"] = len(pending_drop_items)
    stats["drop_terms"] = [item.get("term") for item in pending_drop_items]
    stats["resolved_only"] = args.resolved_only
    print(json.dumps(stats, ensure_ascii=False, indent=2))
    if args.write:
        drop_stats = add_drop_terms(
            drop_path,
            [item["term"] for item in pending_drop_items],
        )
        print(json.dumps(drop_stats, ensure_ascii=False, indent=2))
        if new_text != glossary_text:
            glossary_path.write_text(new_text, encoding="utf-8")
            print(f"wrote: {glossary_path}")
        else:
            print(f"unchanged: {glossary_path}")
        if (args.resolved_only and not args.keep_review) or pending_drop_items:
            cleanup = remove_processed_items(
                review,
                imported_terms,
                remove_skip=args.resolved_only and not args.keep_review,
            )
            review_path.write_text(
                json.dumps(review, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            print(json.dumps(cleanup, ensure_ascii=False, indent=2))
        elif args.resolved_only:
            print("review retained for glossary_refs update")
    else:
        print("dry-run only; pass --write to update glossary")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

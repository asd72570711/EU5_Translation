from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path
from typing import Any


VALID_STATUSES = {"todo", "ai", "cont", "skip", "drop"}
REQUIRED_ITEM_FIELDS = {
    "term",
    "translation",
    "status",
    "category",
    "keys",
    "note",
    "glossary_refs",
}


def validate_review(review: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(review, dict):
        return ["review root must be an object"]

    items = review.get("items")
    if not isinstance(items, list):
        return ["items must be an array"]

    seen_terms: dict[str, int] = {}
    for index, item in enumerate(items):
        label = f"items[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{label} must be an object")
            continue

        missing = REQUIRED_ITEM_FIELDS - set(item)
        for field in sorted(missing):
            errors.append(f"{label} missing field: {field}")

        term = item.get("term")
        if not isinstance(term, str) or not term.strip():
            errors.append(f"{label}.term must be a non-empty string")
        else:
            term_key = term.casefold()
            if term_key in seen_terms:
                errors.append(
                    f"duplicate term: {term} (items[{seen_terms[term_key]}] and {index})"
                )
            else:
                seen_terms[term_key] = index

        for field in ("translation", "category", "note"):
            if field in item and not isinstance(item[field], str):
                errors.append(f"{label}.{field} must be a string")

        status = item.get("status")
        if status not in VALID_STATUSES:
            errors.append(f"{label}.status is invalid: {status!r}")

        keys = item.get("keys")
        if not isinstance(keys, list) or not all(isinstance(key, str) for key in keys):
            errors.append(f"{label}.keys must be an array of strings")

        refs = item.get("glossary_refs")
        if not isinstance(refs, list):
            errors.append(f"{label}.glossary_refs must be an array")
        else:
            for ref_index, ref in enumerate(refs):
                ref_label = f"{label}.glossary_refs[{ref_index}]"
                if not isinstance(ref, dict):
                    errors.append(f"{ref_label} must be an object")
                    continue
                if not isinstance(ref.get("term"), str) or not ref.get("term", "").strip():
                    errors.append(f"{ref_label}.term must be a non-empty string")
                if not isinstance(ref.get("translation"), str):
                    errors.append(f"{ref_label}.translation must be a string")

    source_files = review.get("source_file", [])
    if not isinstance(source_files, list) or not all(
        isinstance(path, str) for path in source_files
    ):
        errors.append("source_file must be an array of strings")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate glossary review JSON without semantic classification or writes."
    )
    parser.add_argument("--review", default="work/glossary_review/review.json")
    # Kept for compatibility with older commands. This script never writes.
    parser.add_argument("--write", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--existing-only", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--source-root", help=argparse.SUPPRESS)
    parser.add_argument("--glossary", help=argparse.SUPPRESS)
    args = parser.parse_args()

    sys.stdout.reconfigure(encoding="utf-8")
    review_path = Path(args.review)
    try:
        review = json.loads(review_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"validation": "failed", "error": str(exc)}, ensure_ascii=False))
        return 1

    errors = validate_review(review)
    items = review.get("items", []) if isinstance(review, dict) else []
    counts = collections.Counter(
        item.get("status", "") for item in items if isinstance(item, dict)
    )
    report = {
        "items": len(items),
        "status": dict(counts),
        "validation": "passed" if not errors else "failed",
        "semantic_classification": False,
        "written": False,
    }
    if errors:
        report["errors"] = errors
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if args.write:
        print("warning: --write is ignored; this script is validation-only", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

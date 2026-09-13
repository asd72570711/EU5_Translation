from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from scan_glossary_candidates import (
    ACRONYM_RE,
    LOWERCASE_NAME_PARTICLES,
    NAME_TITLE_PREFIXES,
    candidates,
    glossary_entries,
    normalized_reference_term,
    parse_entries,
    reference_entries,
    reference_forms,
    resolve_source_files,
)


DEFAULT_REVIEW = "work/glossary_review/review.json"
DEFAULT_GLOSSARY = "translation_glossary.yml"
DEFAULT_SOURCE_ROOT = "source/english"
DEFAULT_REPORT = "work/glossary_review/coverage_audit.json"
DEFAULT_SKIP_HISTORY = "work/glossary_review/skip_history.json"


def load_skip_history(path: Path | None) -> dict[str, set[str]]:
    if path is None or not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("items"), list):
        raise ValueError(f"invalid skip history: {path}")

    history: dict[str, set[str]] = {}
    for item in data["items"]:
        if not isinstance(item, dict) or not item.get("term"):
            continue
        normalized = normalized_reference_term(str(item["term"]))
        if not normalized:
            continue
        history.setdefault(normalized, set()).update(
            key
            for key in item.get("keys", [])
            if isinstance(key, str) and key
        )
    return history


def resolve_review_sources(source_root: Path, source_files: list[str]) -> list[Path]:
    resolved: set[Path] = set()
    for requested in source_files:
        paths = resolve_source_files(source_root, requested)
        if not paths:
            # Accept a review created by an older scanner that stored the
            # source/english prefix instead of a path relative to source_root.
            prefix = f"{source_root.name}/"
            if requested.replace("\\", "/").startswith(prefix):
                paths = resolve_source_files(source_root, requested[len(prefix) :])
        resolved.update(paths)
    return sorted(resolved)


def candidate_confidence(term: str) -> tuple[str, str]:
    words = term.split()
    lowered = term.casefold()
    if any(ord(char) > 127 for char in term):
        return "high", "diacritic or extended Latin candidate"
    if "-" in term or "'" in term or "\u2019" in term:
        return "high", "hyphenated or possessive candidate"
    if ACRONYM_RE.fullmatch(term):
        return "high", "acronym or abbreviation"
    if lowered in NAME_TITLE_PREFIXES or (
        words and words[0].casefold() in NAME_TITLE_PREFIXES and len(words) > 1
    ):
        return "high", "title candidate"
    if re.search(rf"\b(?:{LOWERCASE_NAME_PARTICLES})\b", term):
        return "high", "name-particle candidate"
    if len(words) > 1:
        return "normal", "multiword candidate requiring AI review"
    return "normal", "single-word candidate requiring AI review"


def audit(
    review_path: Path,
    glossary_path: Path,
    source_root: Path,
    skip_history_path: Path | None = None,
) -> dict[str, object]:
    review = json.loads(review_path.read_text(encoding="utf-8"))
    glossary = glossary_entries(glossary_path)
    glossary.update(reference_entries(glossary_path))
    review_items = review.get("items", [])
    review_terms = {
        normalized_reference_term(str(item.get("term", "")))
        for item in review_items
        if isinstance(item, dict) and item.get("term")
    }
    glossary_terms = {
        normalized_reference_term(term) for term in glossary if term
    }
    covered_terms = glossary_terms | review_terms
    skip_history = load_skip_history(skip_history_path)

    source_files = review.get("source_file", [])
    if not isinstance(source_files, list) or not all(
        isinstance(path, str) for path in source_files
    ):
        raise ValueError("review source_file must be an array of strings")
    paths = resolve_review_sources(source_root, source_files)
    if not paths:
        raise ValueError("no source files from review.json matched source root")

    found: dict[str, set[str]] = {}
    found_files: dict[str, set[str]] = {}
    found_key_files: dict[str, dict[str, set[str]]] = {}
    for path in paths:
        relative = path.relative_to(source_root).as_posix()
        for term, keys in candidates(parse_entries(path)).items():
            found.setdefault(term, set()).update(keys)
            found_files.setdefault(term, set()).add(relative)
            key_files = found_key_files.setdefault(term, {})
            for key in keys:
                key_files.setdefault(key, set()).add(relative)

    missing: list[dict[str, object]] = []
    covered = 0
    skip_history_filtered_candidates = 0
    skip_history_filtered_keys = 0
    for term, keys in found.items():
        normalized = normalized_reference_term(term)
        is_covered = any(
            normalized in reference_forms(known) or known in reference_forms(term)
            for known in covered_terms
        )
        if is_covered:
            covered += 1
            continue
        skipped_keys = skip_history.get(normalized, set())
        remaining_keys = keys - skipped_keys
        filtered_key_count = len(keys) - len(remaining_keys)
        skip_history_filtered_keys += filtered_key_count
        if not remaining_keys:
            covered += 1
            skip_history_filtered_candidates += 1
            continue
        confidence, reason = candidate_confidence(term)
        remaining_files = {
            source_file
            for key in remaining_keys
            for source_file in found_key_files.get(term, {}).get(key, set())
        }
        missing.append(
            {
                "term": term,
                "keys": sorted(remaining_keys),
                "source_files": sorted(remaining_files or found_files[term]),
                "confidence": confidence,
                "reason": reason,
            }
        )

    missing.sort(key=lambda item: (item["confidence"] != "high", str(item["term"]).casefold()))
    high_confidence = sum(item["confidence"] == "high" for item in missing)
    return {
        "source_files": [path.relative_to(source_root).as_posix() for path in paths],
        "review_items": len(review_items),
        "glossary_terms": len(glossary_terms),
        "scanned_candidates": len(found),
        "covered_candidates": covered,
        "missing_candidates": len(missing),
        "high_confidence_missing": high_confidence,
        "skip_history_items": len(skip_history),
        "skip_history_filtered_candidates": skip_history_filtered_candidates,
        "skip_history_filtered_keys": skip_history_filtered_keys,
        "missing": missing,
        "writes_review": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit source coverage against glossary and review terms."
    )
    parser.add_argument("--review", default=DEFAULT_REVIEW)
    parser.add_argument("--glossary", default=DEFAULT_GLOSSARY)
    parser.add_argument("--source-root", default=DEFAULT_SOURCE_ROOT)
    parser.add_argument("--report", default=DEFAULT_REPORT)
    parser.add_argument("--skip-history", default=DEFAULT_SKIP_HISTORY)
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()

    sys.stdout.reconfigure(encoding="utf-8")
    try:
        report = audit(
            Path(args.review),
            Path(args.glossary),
            Path(args.source_root).resolve(),
            Path(args.skip_history),
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"audit": "failed", "error": str(exc)}, ensure_ascii=False))
        return 1

    if args.write_report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report["report"] = str(report_path)
        report_path.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    if args.summary:
        summary = {
            key: report[key]
            for key in (
                "review_items",
                "glossary_terms",
                "scanned_candidates",
                "covered_candidates",
                "missing_candidates",
                "high_confidence_missing",
                "skip_history_items",
                "skip_history_filtered_candidates",
                "skip_history_filtered_keys",
            )
        }
        if "report" in report:
            summary["report"] = report["report"]
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

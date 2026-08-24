from __future__ import annotations

import argparse
import json
from pathlib import Path

from scan_glossary_candidates import glossary_alias_groups, glossary_entries, glossary_refs, reference_entries

DEFAULT_MAX_REFS = 12
DEFAULT_CORE_MAX_REFS = 3


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review", default="work/glossary_review/review.json")
    parser.add_argument("--glossary", default="translation_glossary.yml")
    parser.add_argument("--max-refs", type=int, default=DEFAULT_MAX_REFS)
    parser.add_argument("--core-max-refs", type=int, default=DEFAULT_CORE_MAX_REFS)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    review_path = Path(args.review)
    review = json.loads(review_path.read_text(encoding="utf-8"))
    glossary_path = Path(args.glossary)
    glossary = glossary_entries(glossary_path)
    glossary.update(reference_entries(glossary_path))
    alias_groups = glossary_alias_groups(glossary_path)
    changed = 0
    for item in review.get("items", []):
        refs = glossary_refs(
            str(item.get("term", "")),
            glossary,
            limit=args.max_refs,
            core_limit=args.core_max_refs,
            alias_groups=alias_groups,
        )
        if item.get("glossary_refs") != refs:
            item["glossary_refs"] = refs
            changed += 1

    if args.write:
        review_path.write_text(json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "items": len(review.get("items", [])),
        "updated_refs": changed,
        "max_refs": args.max_refs,
        "core_max_refs": args.core_max_refs,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

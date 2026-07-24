from __future__ import annotations

import argparse
import json
from pathlib import Path

from scan_glossary_candidates import glossary_entries, glossary_refs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review", default="work/glossary_review/review.json")
    parser.add_argument("--glossary", default="translation_glossary.yml")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    review_path = Path(args.review)
    review = json.loads(review_path.read_text(encoding="utf-8"))
    glossary = glossary_entries(Path(args.glossary))
    changed = 0
    for item in review.get("items", []):
        refs = glossary_refs(str(item.get("term", "")), glossary)
        if item.get("glossary_refs") != refs:
            item["glossary_refs"] = refs
            changed += 1

    if args.write:
        review_path.write_text(json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"items": len(review.get("items", [])), "updated_refs": changed}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path


DEFAULT_REVIEW = Path("work/glossary_review/review.json")
VALID_STATUSES = {"todo", "ai", "cont", "skip", "drop"}
CONTROL_VALUES = {"ai", "cont", "skip", "drop"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review", default=str(DEFAULT_REVIEW))
    args = parser.parse_args()

    sys.stdout.reconfigure(encoding="utf-8")

    review_path = Path(args.review)
    review = json.loads(review_path.read_text(encoding="utf-8"))
    items = review.get("items", [])

    statuses = collections.Counter(item.get("status", "") for item in items)
    invalid = [item for item in items if item.get("status") not in VALID_STATUSES]
    blank_todo = [
        item for item in items
        if item.get("status") == "todo" and not item.get("translation", "").strip()
    ]
    blank_ai = [
        item for item in items
        if item.get("status") == "ai" and not item.get("translation", "").strip()
    ]
    blank_cont = [
        item for item in items
        if item.get("status") == "cont" and not item.get("translation", "").strip()
    ]
    control_translation = [
        item for item in items
        if item.get("status") == "todo"
        and item.get("translation", "").strip().lower() in CONTROL_VALUES
    ]
    ready = [
        item for item in items
        if item.get("status") in {"todo", "ai"} and item.get("translation", "").strip()
    ]

    print(json.dumps({
        "items": len(items),
        "status": dict(statuses),
        "invalid_status": len(invalid),
        "blank_todo": len(blank_todo),
        "blank_ai": len(blank_ai),
        "blank_cont": len(blank_cont),
        "control_translation": len(control_translation),
        "ready_to_import": len(ready),
        "pending_contextual": statuses.get("cont", 0),
    }, ensure_ascii=False, indent=2))

    for label, rows in (
        ("invalid_status", invalid),
        ("blank_todo", blank_todo),
        ("blank_ai", blank_ai),
        ("blank_cont", blank_cont),
        ("control_translation", control_translation),
    ):
        if rows:
            print(label + ":")
            for item in rows:
                print(f"  - {item.get('term')} [{item.get('status')}]")

    return 1 if invalid or blank_todo or blank_ai or blank_cont or control_translation else 0


if __name__ == "__main__":
    raise SystemExit(main())

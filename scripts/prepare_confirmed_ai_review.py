#!/usr/bin/env python3
"""Treat non-empty ai suggestions as confirmed todo entries."""

import json
from pathlib import Path

path = Path("work/glossary_review/review.json")
data = json.loads(path.read_text(encoding="utf-8"))
changed = 0
for item in data.get("items", []):
    if item.get("status") == "ai" and item.get("translation", "").strip():
        item["status"] = "todo"
        changed += 1
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"converted confirmed ai: {changed}")

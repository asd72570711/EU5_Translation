#!/usr/bin/env python3
"""Remove review items whose cont rules were already written to the glossary."""

import json
from pathlib import Path

path = Path("work/glossary_review/review.json")
data = json.loads(path.read_text(encoding="utf-8"))
before = len(data.get("items", []))
data["items"] = [item for item in data.get("items", []) if item.get("status") != "cont"]
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"removed cont: {before - len(data['items'])}")

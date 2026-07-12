#!/usr/bin/env python3
"""AI pre-screen obvious ordinary QA/debug text in review.json."""

import json
from pathlib import Path

PATH = Path("work/glossary_review/review.json")
SKIP = {
    "All I", "Another", "ASAP", "Become the Leader", "Close Menu",
    "Create the Test Rebels", "Decolonize Africa", "Decolonize Asia",
    "Decolonize Europe", "Decolonize North America", "Decolonize Oceania",
    "Decolonize Random New World", "Decolonize South America", "Deploy ALL",
    "Destroy ALL the Rebels", "IMMEDIATELY", "Kill ALL", "Main Title Lorem",
    "NOT", "Only the Heretics", "Others", "RIGHT NOW", "Select", "Test Rebels",
    "THAT", "This", "Which Artist", "Which Empire", "Which Heir",
    "Which Ruler", "WILL", "Woman", "World", "World Conquest",
    "World Conquest Menu",
}

data = json.loads(PATH.read_text(encoding="utf-8"))
changed = 0
for item in data.get("items", []):
    if item.get("term") in SKIP and item.get("status") == "todo":
        item["status"] = "skip"
        changed += 1

PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"marked skip: {changed}")

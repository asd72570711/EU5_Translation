#!/usr/bin/env python3
"""AI pre-screen obvious non-glossary candidates in religion_review.json."""

import json
from pathlib import Path

PATH = Path("work/glossary_review/religion_review.json")

SKIP = {
    "Capital",
    "Celebrates",
    "Corrupt Priest",
    "Demands Sacrifice",
    "Displeased",
    "Expansion of Religious Grounds",
    "Epics of History",
    "Fear and Hunger",
    "Front",
    "Gods Disapprove of War",
    "Hear Our Plea",
    "In Brightest Day",
    "In Darkest Night",
    "Monstrous Birth",
    "Neglects",
    "Neglects Rites",
    "Philosopher's Paradox",
    "Plenty",
    "Remove the Monist",
    "Smiles Upon Us",
    "Talisman",
    "The Blessing",
    "The Christian Question",
    "The Eagle",
    "The Wisdom",
    "Way of the Ancestors.' This",
}

data = json.loads(PATH.read_text(encoding="utf-8"))
changed = 0
for item in data["items"]:
    if item["term"] in SKIP and item["status"] == "todo":
        item["status"] = "skip"
        changed += 1

PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"marked skip: {changed}")

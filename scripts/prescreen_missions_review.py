import json
from pathlib import Path


REVIEW_PATH = Path("work/glossary_review/review.json")

# These are one-off generic event headings or obvious UI-fragment candidates,
# not reusable terminology. Ambiguous mission and mechanic names remain.
SKIP_TERMS = {
    "Annexation Proceedings",
    "Approve of Societal Progress",
    "Bring Growth",
    "Colony Gains Traction",
    "Cultural Learnings",
    "Cultural Spread",
    "Decentralization",
    "Diplomatic Incident",
    "Diplomatic Ties",
    "Donation",
    "Foreign Interference",
    "Friction Between",
    "Growth of the Industry",
    "Integration Progress",
    "Integration Resistance",
    "Local Demand Collaboration",
    "Mind",
    "Protest the War Chest",
    "Religious Spread",
    "Resists Centralization",
    "Resists Urbanization",
    "Rivaling Adventurers",
    "Rural Folk Left Behind",
    "Rural Neglect",
    "Taxation Reforms",
    "The Development of Trade",
    "The Future of Exploration",
    "The Growth",
    "The Library",
    "The Mind",
    "The Ravages of War",
    "The Scholars",
    "The Winds of Trade",
    "To War",
    "War Effort",
    "War Innovations",
    "War Loans",
    "Automation Cog To",
    "Bribe Button",
    "Build Button",
    "Button",
    "Click Plus Button",
    "Country Card Declare War Button",
    "Country Card Spy Network Button",
    "Foreign Country Panel",
    "In the Panel",
    "Possible Rivals Alert",
    "Rivals Button",
}


def main() -> None:
    data = json.loads(REVIEW_PATH.read_text(encoding="utf-8"))
    changed = []
    for item in data["items"]:
        if item.get("status") == "todo" and item.get("term") in SKIP_TERMS:
            item["status"] = "skip"
            changed.append(item["term"])
    REVIEW_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"marked_skip: {len(changed)}")
    for term in changed:
        print(term)


if __name__ == "__main__":
    main()

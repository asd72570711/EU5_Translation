import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "import_glossary_review.py"


class ImportGlossaryReviewTests(unittest.TestCase):
    def test_keep_review_only_removes_drop_items_early(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            review = root / "review.json"
            glossary = root / "glossary.yml"
            drop_terms = root / "drop.yml"
            review.write_text(
                json.dumps(
                    {
                        "items": [
                            {
                                "term": "Confirmed Term",
                                "translation": "confirmed",
                                "status": "todo",
                            },
                            {
                                "term": "Discarded Term",
                                "translation": "",
                                "status": "drop",
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            glossary.write_text(
                "fixed:\n\naliases:\n\ncontextual:\n\nreference_terms:\n",
                encoding="utf-8",
            )
            drop_terms.write_text("drop_terms:\n", encoding="utf-8")

            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--review",
                    str(review),
                    "--glossary",
                    str(glossary),
                    "--drop-terms",
                    str(drop_terms),
                    "--resolved-only",
                    "--keep-review",
                    "--write",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            remaining = json.loads(review.read_text(encoding="utf-8"))["items"]
            self.assertEqual([item["term"] for item in remaining], ["Confirmed Term"])
            self.assertIn('  - "Discarded Term"', drop_terms.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

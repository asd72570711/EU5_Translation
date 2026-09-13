import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_glossary_review_coverage.py"


class AuditGlossaryReviewCoverageTests(unittest.TestCase):
    def test_skip_history_filters_only_previously_reviewed_keys(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_root = root / "source"
            source_root.mkdir()
            (source_root / "sample.yml").write_text(
                'l_english:\n event.1.desc: "Persistent Term"\n'
                ' event.2.desc: "Persistent Term"\n',
                encoding="utf-8",
            )
            review = root / "review.json"
            review.write_text(
                json.dumps({"source_file": ["sample.yml"], "items": []}),
                encoding="utf-8",
            )
            glossary = root / "glossary.yml"
            glossary.write_text(
                "fixed:\n\naliases:\n\ncontextual:\n\nreference_terms:\n",
                encoding="utf-8",
            )
            skip_history = root / "skip_history.json"
            skip_history.write_text(
                json.dumps(
                    {
                        "version": 1,
                        "items": [
                            {"term": "Persistent Term", "keys": ["event.1.desc"]}
                        ],
                    }
                ),
                encoding="utf-8",
            )
            report = root / "coverage.json"

            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--review",
                    str(review),
                    "--glossary",
                    str(glossary),
                    "--source-root",
                    str(source_root),
                    "--skip-history",
                    str(skip_history),
                    "--report",
                    str(report),
                    "--write-report",
                    "--summary",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            data = json.loads(report.read_text(encoding="utf-8"))
            candidate = next(
                item for item in data["missing"] if item["term"] == "Persistent Term"
            )
            self.assertEqual(candidate["keys"], ["event.2.desc"])
            self.assertEqual(data["skip_history_filtered_keys"], 1)

            skip_history.write_text(
                json.dumps(
                    {
                        "version": 1,
                        "items": [
                            {
                                "term": "Persistent Term",
                                "keys": ["event.1.desc", "event.2.desc"],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--review",
                    str(review),
                    "--glossary",
                    str(glossary),
                    "--source-root",
                    str(source_root),
                    "--skip-history",
                    str(skip_history),
                    "--report",
                    str(report),
                    "--write-report",
                    "--summary",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            data = json.loads(report.read_text(encoding="utf-8"))
            self.assertFalse(
                any(item["term"] == "Persistent Term" for item in data["missing"])
            )
            self.assertEqual(data["skip_history_filtered_candidates"], 1)
            self.assertEqual(data["skip_history_filtered_keys"], 2)


if __name__ == "__main__":
    unittest.main()

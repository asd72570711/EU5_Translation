import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.scan_glossary_candidates import (
    candidates,
    glossary_alias_groups,
    glossary_entries,
    glossary_refs,
)


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "scan_glossary_candidates.py"


class ScanGlossaryCandidatesTests(unittest.TestCase):
    def test_alias_entry_allows_trailing_comment(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            glossary = Path(directory) / "glossary.yml"
            glossary.write_text(
                "fixed:\n\n"
                "aliases:\n"
                "  Meissen:  # official spelling\n"
                '    zh: "Meissen ZH"\n'
                "    also:\n"
                "      - Meissen Alt\n\n"
                "contextual:\n\n"
                "reference_terms:\n",
                encoding="utf-8",
            )

            entries = glossary_entries(glossary)
            groups = glossary_alias_groups(glossary)

            self.assertEqual(entries["Meissen"], "Meissen ZH")
            self.assertEqual(entries["Meissen Alt"], "Meissen ZH")
            self.assertEqual(groups["meissen"], groups["meissen alt"])
            self.assertIn(
                {"term": "Meissen", "translation": "Meissen ZH"},
                glossary_refs(
                    "Margrave of Meissen",
                    entries,
                    alias_groups=groups,
                ),
            )

    def test_links_ist_ic_ism_concept_family_refs(self) -> None:
        noun_glossary = {
            "Neoplatonism": "Neoplatonism ZH",
            "Neoplatonist": "Neoplatonist ZH",
        }
        adjective_glossary = {"Neoplatonic": "Neoplatonic ZH"}

        refs = glossary_refs("Neoplatonic", noun_glossary)

        self.assertIn(
            {"term": "Neoplatonism", "translation": "Neoplatonism ZH"},
            refs,
        )
        self.assertIn(
            {"term": "Neoplatonist", "translation": "Neoplatonist ZH"},
            refs,
        )
        self.assertIn(
            {"term": "Neoplatonic", "translation": "Neoplatonic ZH"},
            glossary_refs("Neoplatonism", adjective_glossary),
        )
        self.assertIn(
            {"term": "Neoplatonic", "translation": "Neoplatonic ZH"},
            glossary_refs("Neoplatonist", adjective_glossary),
        )

    def test_keeps_names_at_end_of_comma_list(self) -> None:
        text = (
            "Properties include Fosen, Frosta, Stjørdal, Sunnmøre, Romsdal, "
            "Edøy, Selbu and Herjedalen. He has accepted the post."
        )

        found = candidates([("flavor_nor.2.desc", text)])

        for term in ("Stjørdal", "Selbu", "Herjedalen"):
            self.assertIn(term, found)
        self.assertFalse(any(". He" in term for term in found))

    def test_does_not_split_non_list_coordinated_name(self) -> None:
        found = candidates(
            [("example", "Trinidad and Tobago has entered the agreement.")]
        )

        self.assertIn("Trinidad and Tobago", found)
        self.assertNotIn("Trinidad", found)
        self.assertNotIn("Tobago", found)

    def test_does_not_drop_leading_name_particles(self) -> None:
        found = candidates(
            [
                (
                    "arabic.place",
                    "The battle of al-Qa\u015fr al-Kab\u012br ended in defeat.",
                ),
                (
                    "arabic.person",
                    "Abu al-Qasim al-Zahrawi served at court.",
                ),
                ("european.person", "The paintings of van Gogh are renowned."),
            ]
        )

        self.assertIn("al-Qa\u015fr al-Kab\u012br", found)
        self.assertNotIn("Qa\u015fr al-Kab\u012br", found)
        self.assertIn("Abu al-Qasim al-Zahrawi", found)
        self.assertNotIn("al-Qasim al-Zahrawi", found)
        self.assertNotIn("Qasim al-Zahrawi", found)
        self.assertIn("van Gogh", found)
        self.assertNotIn("Gogh", found)

    def test_keeps_short_name_when_it_appears_independently(self) -> None:
        found = candidates(
            [
                ("full", "The battle of al-Qa\u015fr al-Kab\u012br ended in defeat."),
                ("short", "Qa\u015fr al-Kab\u012br later recovered."),
            ]
        )

        self.assertIn("al-Qa\u015fr al-Kab\u012br", found)
        self.assertIn("Qa\u015fr al-Kab\u012br", found)

    def test_still_extracts_place_from_government_name(self) -> None:
        found = candidates(
            [("example", "The Kingdom of Georgia entered the conflict.")]
        )

        self.assertIn("Kingdom of Georgia", found)
        self.assertIn("Georgia", found)

    def test_does_not_treat_english_function_words_as_name_particles(self) -> None:
        found = candidates(
            [
                (
                    "example",
                    "He was known as Catherine, served as King, met an Italian, "
                    "and arrived at Deptford.",
                )
            ]
        )

        for fragment in ("as Catherine", "as King", "an Italian", "at Deptford"):
            self.assertNotIn(fragment, found)

    def test_keeps_common_title_abbreviation(self) -> None:
        found = candidates([("example", "The church of St. Peter is renowned.")])

        self.assertIn("St. Peter", found)

    def test_skip_history_resets_only_after_review_is_written(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_root = root / "source"
            source_root.mkdir()
            (source_root / "sample.yml").write_text(
                'l_english:\n example: "Persistent Candidate"\n',
                encoding="utf-8",
            )
            glossary = root / "glossary.yml"
            glossary.write_text(
                "fixed:\n\naliases:\n\ncontextual:\n\nreference_terms:\n",
                encoding="utf-8",
            )
            drop_terms = root / "drop.yml"
            drop_terms.write_text("drop_terms:\n", encoding="utf-8")
            review = root / "review.json"
            skip_history = root / "skip_history.json"
            original_history = {
                "version": 1,
                "items": [{"term": "Old Candidate", "keys": ["old.key"]}],
            }
            skip_history.write_text(
                json.dumps(original_history), encoding="utf-8"
            )
            command = [
                sys.executable,
                str(SCRIPT),
                "--file",
                "sample.yml",
                "--source-root",
                str(source_root),
                "--glossary",
                str(glossary),
                "--drop-terms",
                str(drop_terms),
                "--review-output",
                str(review),
                "--skip-history",
                str(skip_history),
                "--reset-skip-history",
            ]

            subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(
                json.loads(skip_history.read_text(encoding="utf-8")),
                original_history,
            )

            subprocess.run(
                command + ["--write-review"],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertTrue(review.exists())
            self.assertEqual(
                json.loads(skip_history.read_text(encoding="utf-8")),
                {"version": 1, "items": []},
            )


if __name__ == "__main__":
    unittest.main()

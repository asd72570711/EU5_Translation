from __future__ import annotations

import unittest

from scripts.prescreen_glossary_review import validate_review


class ValidateReviewTests(unittest.TestCase):
    def test_category_is_optional_for_new_review_items(self) -> None:
        review = {
            "source_file": ["example_l_english.yml"],
            "items": [
                {
                    "term": "Example",
                    "translation": "",
                    "status": "todo",
                    "keys": ["example_key"],
                    "note": "",
                    "glossary_refs": [],
                }
            ],
        }

        self.assertEqual(validate_review(review), [])

    def test_legacy_category_is_still_validated_when_present(self) -> None:
        review = {
            "source_file": [],
            "items": [
                {
                    "term": "Example",
                    "translation": "",
                    "status": "todo",
                    "category": None,
                    "keys": [],
                    "note": "",
                    "glossary_refs": [],
                }
            ],
        }

        self.assertIn("items[0].category must be a string", validate_review(review))


if __name__ == "__main__":
    unittest.main()

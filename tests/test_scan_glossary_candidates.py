import unittest

from scripts.scan_glossary_candidates import candidates


class ScanGlossaryCandidatesTests(unittest.TestCase):
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

    def test_keeps_common_title_abbreviation(self) -> None:
        found = candidates([("example", "The church of St. Peter is renowned.")])

        self.assertIn("St. Peter", found)


if __name__ == "__main__":
    unittest.main()

import unittest
from brfss_diabetes_surveys_etl.src.main.scripts.cleaners.description_cleaner import (
    DescriptionCleaner,
)


class TestDescriptionCleaner(unittest.TestCase):
    def setUp(self):
        self.raw_description = """
        SAS    Variable   Name: AGE
        Section   Name: DEMO�
        More\xa0text with non-breaking spaces
        """

    def test_init_fails(self):
        test_cases = [("", "empty"), ("\n\t", "whitespace")]
        for invalid_input, description in test_cases:
            with self.subTest(description=description):
                with self.assertRaises(ValueError):
                    DescriptionCleaner(invalid_input)

    def test_clean_success(self):
        cleaner = DescriptionCleaner(self.raw_description)
        cleaner.clean()
        expected = """
        SAS Variable Name: AGE
        Section Name: DEMO
        More text with non-breaking spaces
        """
        self.assertEqual(cleaner.clean_description.strip(), expected.strip())

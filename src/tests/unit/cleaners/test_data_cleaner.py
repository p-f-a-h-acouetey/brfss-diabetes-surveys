import unittest
import pandas as pd
from src.main.scripts.cleaners.data_cleaner import DataCleaner


class TestDataCleaner(unittest.TestCase):
    def setUp(self):
        self.raw_df = pd.DataFrame(
            {
                "_LLCPWT": [1.2, 1.1, 1.3, 1.6],
                "DIABETE4": [1, 4, 1, 4],
            }
        )
        self.clean_description = """
        Section Name: Calculated Variables
        Description: Sampling weight.
        SAS Variable Name: _LLCPWT
        """

    def test_init_fails(self):
        test_cases = [
            (pd.DataFrame(), self.clean_description, "empty dataframe"),
            (self.raw_df, "", "empty description"),
            (self.raw_df, "   \n\t  ", "whitespace description"),
        ]
        for df, desc, case_name in test_cases:
            with self.subTest(case=case_name):
                with self.assertRaises(ValueError):
                    DataCleaner(df, desc)

    def test_clean_empty_result_fails(self):
        tiny_df = pd.DataFrame({"_LLCPWT": [1.0]})
        cleaner = DataCleaner(tiny_df, self.clean_description)
        with self.assertRaises(ValueError):
            cleaner.clean()  # Should remove _LLCPWT and leave empty DF

    def test_clean_success(self):
        cleaner = DataCleaner(self.raw_df, self.clean_description)
        cleaner.clean()
        result_df = cleaner.df.sort_values(by=["DIABETE4"]).reset_index(drop=True)
        expected_result_df = (
            pd.DataFrame({"DIABETE4": pd.Categorical([1, 2])})
            .sort_values(by=["DIABETE4"])
            .reset_index(drop=True)
        )
        pd.testing.assert_frame_equal(result_df, expected_result_df)

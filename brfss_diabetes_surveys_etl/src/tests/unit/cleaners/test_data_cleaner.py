import unittest
import pandas as pd
from unittest.mock import patch
from brfss_diabetes_surveys_etl.src.main.scripts.cleaners.data_cleaner import (
    DataCleaner,
)


class TestDataCleaner(unittest.TestCase):
    def setUp(self):
        self.raw_df = pd.DataFrame(
            {
                "_LLCPWT": [1.2, 1.1, 1.3, 1.6],
                "DIABETE4": [1, 4, 1, 4],
            }
        )

    def test_init_fails(self):
        test_cases = [
            (pd.DataFrame(), "empty dataframe 1"),
            (pd.DataFrame(columns=["_LLCPWT"]), "empty dataframe 2"),
        ]
        for raw_df, case_name in test_cases:
            with self.subTest(case=case_name):
                with self.assertRaises(ValueError):
                    DataCleaner(raw_df)

    @patch.dict(
        "brfss_diabetes_surveys_etl.src.main.configs.cleaners.data_cleaner.CLEANING_CONFIGS",
        {
            "bfrss_chronic_health_conditions_vars": ["DIABETE4"]
        },  # Control on CLEANING_CONFIGS for only 'DIABETE4'
        clear=True,
    )
    def test_clean_success(self):
        cleaner = DataCleaner(self.raw_df)
        cleaner.clean_data()
        result_df = cleaner.df.sort_values(by="DIABETE4").reset_index(drop=True)
        expected_df = (
            pd.DataFrame({"DIABETE4": [1, 4]})
            .sort_values(by="DIABETE4")
            .reset_index(drop=True)
        )
        pd.testing.assert_frame_equal(result_df, expected_df)

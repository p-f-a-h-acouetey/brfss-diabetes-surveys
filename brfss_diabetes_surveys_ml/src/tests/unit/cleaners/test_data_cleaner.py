import unittest
import numpy as np
import pandas as pd
from unittest.mock import patch
from brfss_diabetes_surveys_ml.src.main.scripts.cleaners.data_cleaner import (
    DataCleaner,
)
from brfss_diabetes_surveys_ml.src.main.configs.cleaners.data_cleaner import (
    CLEANING_CONFIGS,
)


class TestDataCleaner(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame(
            {
                "DRNKANY6": [1.0, 2.0, 1.0, 1.0],
                "DROCDY4_": [1.0, 0.0, 899.0, 3.0],
                "_AGE80": [18.0, 19.0, 20.0, 80.0],
                "_DRNKWK3": [2.0, 4.0, 99900.0, 15.0],
                "_STATE": [1.0, 2.0, 4.0, 11.0],
                "DIABETE4": [1.0, 3.0, 4.0, 9.0],
            }
        )

    def test_init_fails(self):
        test_cases = [
            (pd.DataFrame(), "empty dataframe 1"),
            (pd.DataFrame(columns=["DROCDY4_"]), "empty dataframe 2"),
        ]
        for df, case_name in test_cases:
            with self.subTest(case=case_name):
                with self.assertRaises(ValueError):
                    DataCleaner(df)

    @patch.dict(
        "brfss_diabetes_surveys_ml.src.main.configs.cleaners.data_cleaner.CLEANING_CONFIGS",
        {
            k: CLEANING_CONFIGS[k]
            for k in [
                "DRNKANY6",
                "DROCDY4_",
                "_AGE80",
                "_DRNKWK3",
                "_STATE",
                "DIABETE4",
            ]
            if k in CLEANING_CONFIGS
        },  # Control on CLEANING_CONFIGS for only required columns
        clear=True,
    )
    def test_clean_success(self):
        cleaner = DataCleaner(self.df)
        cleaner.clean_data()
        result_df = cleaner.df.sort_values(by="diabetic_status").reset_index(drop=True)

        expected_df = (
            (
                pd.DataFrame(
                    {
                        "did_you_have_at_least_1drink_in_last_30days": [
                            "yes",
                            "no",
                            "yes",
                        ],
                        "at_least_1drink_occasion_per_day": ["yes", "no", "yes"],
                        "imputed_age": pd.Series([18, 19, 20], dtype="Int64"),
                        "weekly_number_of_alcoholic_drinks": pd.Series(
                            [2, 4, np.nan], dtype="Int64"
                        ),
                        "state": ["Alabama", "Alaska", "Arizona"],
                        "diabetic_status": ["diabetes", "no diabetes", "prediabetes"],
                    }
                )
            )
            .sort_values(by="diabetic_status")
            .reset_index(drop=True)
        )
        ordered_cols = sorted(list(expected_df.columns))
        expected_df = expected_df[ordered_cols]

        pd.testing.assert_frame_equal(result_df, expected_df)

import unittest
import pandas as pd
from unittest.mock import patch
from brfss_diabetes_surveys_etl.src.main.scripts.sinkers.data_sinker import (
    DataSinker,
)


class TestDataSinker(unittest.TestCase):
    def setUp(self):
        self.clean_df = pd.DataFrame(
            {
                "_SEX": [0, 0, 1, 0],
                "DIABETE4": [1, 4, 1, 4],
            }
        )

    def test_init_fails(self):
        test_cases = [
            (pd.DataFrame(), "empty dataframe 1"),
            (pd.DataFrame(columns=["_SEX"]), "empty dataframe 2"),
        ]
        for clean_df, case_name in test_cases:
            with self.subTest(case=case_name):
                with self.assertRaises(ValueError):
                    DataSinker(clean_df)

    @patch.dict(
        "brfss_diabetes_surveys_etl.src.main.configs.sinkers.data_sinker.SINK_CONFIGS",
        {"path": "/tmp/test_sink", "format": ".parquet"},
        clear=True,
    )
    @patch.object(pd.DataFrame, "to_parquet")
    def test_sink_success(self, mock_to_parquet):
        sinker = DataSinker(self.clean_df)
        sinker.sink_data()
        mock_to_parquet.assert_called_once_with(
            path="/tmp/test_sink/LLCP2024.parquet", index=False
        )

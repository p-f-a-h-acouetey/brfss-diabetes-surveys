import unittest
import pandas as pd
from unittest.mock import patch
from brfss_diabetes_surveys_etl.src.main.scripts.pipelines.etl_pipeline import (
    ETLPipeline,
)


class TestETLPipeline(unittest.TestCase):
    def setUp(self):
        self.raw_data_path = "/fake/data.xpt"

    def test_init_fails(self):
        test_cases = [("", "empty data path"), ("   \n\t", "whitespace data path")]
        for data_path, case_name in test_cases:
            with self.subTest(case=case_name):
                with self.assertRaises(ValueError):
                    ETLPipeline(raw_data_path=data_path)

    @patch(
        "brfss_diabetes_surveys_etl.src.main.scripts.loaders.data_loader.pyreadstat.read_xport"
    )
    @patch.dict(
        "brfss_diabetes_surveys_etl.src.main.configs.cleaners.data_cleaner.CLEANING_CONFIGS",
        {
            "bfrss_chronic_health_conditions_vars": ["DIABETE4"]
        },  # Control on CLEANING_CONFIGS for only 'DIABETE4'
        clear=True,
    )
    def test_run_success(self, mock_read_xport):
        # Mock ONLY XPT reading
        mock_df = pd.DataFrame({"_LLCPWT": [1.2, 1.1, 1.1], "DIABETE4": [1, 4, 4]})
        mock_read_xport.return_value = (mock_df, None)

        # Run pipeline with mocked XPT
        pipeline = ETLPipeline(self.raw_data_path)
        result_df = (pipeline.run()).sort_values(by=["DIABETE4"]).reset_index(drop=True)

        # Verify: _LLCPWT removed, DIABETE4 kept
        expected_df = (
            pd.DataFrame({"DIABETE4": [1, 4]})
            .sort_values(by=["DIABETE4"])
            .reset_index(drop=True)
        )
        pd.testing.assert_frame_equal(result_df, expected_df)

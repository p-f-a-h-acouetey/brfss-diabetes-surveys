import unittest
import pandas as pd
import tempfile
from pathlib import Path
from unittest.mock import patch
from brfss_diabetes_surveys_etl.src.main.scripts.pipelines.etl_pipeline import (
    ETLPipeline,
)


class TestETLPipeline(unittest.TestCase):
    def setUp(self):
        self.raw_data_path = "/fake/data.xpt"
        self.raw_description_path = "/fake/desc.HTML"

    def test_init_empty_paths_fails(self):
        test_cases = [
            ("", self.raw_description_path, "empty data path"),
            (self.raw_data_path, "", "empty description path"),
            (
                "   \n\t",
                self.raw_description_path,
                "whitespace data path",
            ),  # Fixed escapes
            (self.raw_description_path, "\n\t   ", "whitespace description path"),
        ]
        for data_path, desc_path, case_name in test_cases:
            with self.subTest(case=case_name):
                with self.assertRaises(ValueError):
                    ETLPipeline(data_path, desc_path)

    @patch(
        "brfss_diabetes_surveys_etl.src.main.scripts.loaders.data_loader.pyreadstat.read_xport"
    )
    def test_execute(self, mock_read_xport):
        # Create REAL temp description file
        with tempfile.TemporaryDirectory() as tmpdir:
            desc_path = Path(tmpdir) / "desc.HTML"
            desc_content = """
            Section Name: Calculated Variables
            Description: Sampling weight.
            SAS Variable Name: _LLCPWT
            """
            desc_path.write_text(desc_content)

            # Mock ONLY XPT reading
            mock_df = pd.DataFrame({"_LLCPWT": [1.2, 1.1], "DIABETE4": [1, 4]})
            mock_read_xport.return_value = (mock_df, None)

            # Run pipeline with real desc file, mocked XPT
            pipeline = ETLPipeline(self.raw_data_path, str(desc_path))
            result_df = (
                pipeline.execute().sort_values(by=["DIABETE4"]).reset_index(drop=True)
            )

            # Verify: _LLCPWT removed, DIABETE4 cleaned (1->1, 4->2)
            expected_df = (
                pd.DataFrame({"DIABETE4": pd.Categorical([1, 2])})
                .sort_values(by=["DIABETE4"])
                .reset_index(drop=True)
            )
            pd.testing.assert_frame_equal(result_df, expected_df, check_dtype=False)

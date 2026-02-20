import unittest
import pandas as pd
from unittest.mock import patch
from brfss_diabetes_surveys_ml.src.main.scripts.loaders.data_loader import DataLoader


class TestDataLoader(unittest.TestCase):
    def setUp(self):
        self.data_path = "/fake/data.parquet"

    def test_init_fails(self):
        with self.assertRaises(ValueError):
            DataLoader("data.txt")

    @patch(
        "brfss_diabetes_surveys_ml.src.main.scripts.loaders.data_loader.pd.read_parquet"
    )
    def test_read_data_success(self, mock_read_parquet):
        mock_read_parquet.return_value = pd.DataFrame({"test": [1]})
        loader = DataLoader(self.data_path)
        loader.read_data()
        self.assertFalse(loader.df.empty)

    @patch(
        "brfss_diabetes_surveys_ml.src.main.scripts.loaders.data_loader.pd.read_parquet"
    )
    def test_read_data_empty_fails(self, mock_read_parquet):
        mock_read_parquet.return_value = pd.DataFrame()
        loader = DataLoader(self.data_path)
        with self.assertRaises(ValueError):
            loader.read_data()

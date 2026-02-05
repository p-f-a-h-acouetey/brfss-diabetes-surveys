import unittest
import pandas as pd
from unittest.mock import patch
from brfss_diabetes_surveys_etl.src.main.scripts.loaders.data_loader import DataLoader


class TestDataLoader(unittest.TestCase):
    def setUp(self):
        self.raw_data_path = "/fake/data.xpt"

    def test_init_fails(self):
        with self.assertRaises(ValueError):
            DataLoader("data.txt")

    @patch(
        "brfss_diabetes_surveys_etl.src.main.scripts.loaders.data_loader.pyreadstat.read_xport"
    )
    def test_read_data_success(self, mock_read_xport):
        mock_read_xport.return_value = (pd.DataFrame({"test": [1]}), None)
        loader = DataLoader(self.raw_data_path)
        loader.read_data()
        self.assertFalse(loader.raw_df.empty)

    @patch(
        "brfss_diabetes_surveys_etl.src.main.scripts.loaders.data_loader.pyreadstat.read_xport"
    )
    def test_read_data_empty_fails(self, mock_read_xport):
        mock_read_xport.return_value = (pd.DataFrame(), None)
        loader = DataLoader(self.raw_data_path)
        with self.assertRaises(ValueError):
            loader.read_data()

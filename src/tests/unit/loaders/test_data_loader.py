import unittest
import pandas as pd
from unittest.mock import patch
from src.main.scripts.loaders.data_loader import DataLoader
from src.main.configs.loaders.data_loader import DATA_CONFIGS

class TestDataLoader(unittest.TestCase):

    def setUp(self):
        self.data_path = "/fake/data.xpt"
        self.description_path = "/fake/desc.HTML"

    def test_init_fails(self):
        with self.assertRaises(ValueError):
            DataLoader('data.txt', self.description_path)
        with self.assertRaises(ValueError):
            DataLoader(self.data_path, 'desc.txt')

    @patch('src.main.scripts.loaders.data_loader.pyreadstat.read_xport')
    def test_read_data_success(self, mock_read_xport):
        mock_read_xport.return_value = (pd.DataFrame({'test': [1]}), None)
        loader = DataLoader(self.data_path, self.description_path)
        loader._read_data()
        mock_read_xport.assert_called_once_with(self.data_path, encoding=DATA_CONFIGS['encoding'])
        self.assertFalse(loader.data.empty)

    @patch('src.main.scripts.loaders.data_loader.pyreadstat.read_xport')
    def test_read_data_empty_fails(self, mock_read_xport):
        mock_read_xport.return_value = (pd.DataFrame(), None)
        loader = DataLoader(self.data_path, self.description_path)
        with self.assertRaises(ValueError):
            loader._read_data()

    @patch('src.main.scripts.loaders.data_loader.extract_html_text')
    def test_read_description_success(self, mock_extract_html_text):
        mock_extract_html_text.return_value = "Fake text"
        loader = DataLoader(self.data_path, self.description_path)
        loader._read_description()
        mock_extract_html_text.assert_called_once_with(self.description_path)
        self.assertTrue(len(loader.description) > 0)

    @patch('src.main.scripts.loaders.data_loader.extract_html_text')
    def test_read_description_empty_fails(self, mock_extract_html_text):
        mock_extract_html_text.return_value = ""
        loader = DataLoader(self.data_path, self.description_path)
        with self.assertRaises(ValueError):
            loader._read_description()

    @patch('src.main.scripts.loaders.data_loader.extract_html_text')
    @patch('src.main.scripts.loaders.data_loader.pyreadstat.read_xport')
    def test_full_load_success(self, mock_read_xport, mock_extract_html_text):
        mock_read_xport.return_value = (pd.DataFrame({'test': [1]}), None)
        mock_extract_html_text.return_value = "Fake text"
        loader = DataLoader(self.data_path, self.description_path)
        loader.full_load()
        self.assertFalse(loader.data.empty)
        self.assertTrue(len(loader.description) > 0)

    @patch('src.main.scripts.loaders.data_loader.extract_html_text')
    @patch('src.main.scripts.loaders.data_loader.pyreadstat.read_xport')
    def test_full_load_fails_description(self, mock_read_xport, mock_extract_html_text):
        mock_read_xport.return_value = (pd.DataFrame({'test': [1]}), None)
        mock_extract_html_text.return_value = ""

        loader = DataLoader(self.data_path, self.description_path)
        with self.assertRaises(ValueError):
            loader.full_load()

        self.assertFalse(loader.data.empty)
        self.assertIsNone(getattr(loader, 'description', None))

    @patch('src.main.scripts.loaders.data_loader.extract_html_text')
    @patch('src.main.scripts.loaders.data_loader.pyreadstat.read_xport')
    def test_full_load_fails_data(self, mock_read_xport, mock_extract_html_text):
        mock_read_xport.return_value = (pd.DataFrame(), None)
        mock_extract_html_text.return_value = "Fake text"

        loader = DataLoader(self.data_path, self.description_path)
        with self.assertRaises(ValueError):
            loader.full_load()

        self.assertIsNone(getattr(loader, 'data', None))
        self.assertIsNone(getattr(loader, 'description', None))

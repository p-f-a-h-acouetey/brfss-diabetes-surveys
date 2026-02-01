import unittest
from unittest.mock import patch, mock_open
from src.main.scripts.loaders.description_loader import DescriptionLoader


class TestDescriptionLoader(unittest.TestCase):
    def setUp(self):
        self.raw_description_path = "/fake/desc.HTML"

    def test_init_fails(self):
        with self.assertRaises(ValueError):
            DescriptionLoader("desc.txt")

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="""
    <html><body><p>Test content with <script>ignore</script> and styles.</p></body></html>
    """,
    )
    def test_read_description_success(self, mock_file):
        loader = DescriptionLoader(self.raw_description_path)
        loader.read_description()
        expected_text = (
            "Test content with   and styles."  # <script>ignore</script> -> " "
        )
        self.assertEqual(loader.raw_description.strip(), expected_text.strip())

    @patch("builtins.open", new_callable=mock_open, read_data="")
    @patch(
        "builtins.open", new_callable=mock_open, read_data="<html><body></body></html>"
    )
    def test_read_description_fails(self, mock_no_text_file, mock_empty_file):
        # Test empty file
        loader1 = DescriptionLoader(self.raw_description_path)
        with self.assertRaises(ValueError):
            loader1.read_description()

        # Reset for second test
        mock_empty_file.reset_mock()

        # Test no-text HTML
        loader2 = DescriptionLoader(self.raw_description_path)
        with self.assertRaises(ValueError):
            loader2.read_description()

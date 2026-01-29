from bs4 import BeautifulSoup
import os, re, tempfile, unittest
from src.main.scripts.loaders.utils import extract_html_text
from src.main.configs.loaders.data_loader import DESCRIPTION_CONFIGS

class TestUtils(unittest.TestCase):

    def setUp(self):
        # Create temp XPT file (mock binary content)
        self.data_path = tempfile.mktemp(suffix='.xpt')
        with open(self.data_path, 'wb') as file:
            file.write(b'SAS_XPORT_BINARY_DATA')

        # Create temp HTML file with some SAS contents
        self.description_path = tempfile.mktemp(suffix='.HTML')
        html_content = """
        <html><body>
        <script>alert('remove me')</script>
        <style>body {color:red}</style>
        <h1>SAS    Variable   Name: AGE</h1>
        <p>Section   Name: DEMO�</p>
        <p>More\xa0text&nbsp;with non-breaking spaces</p>
        </body></html>
        """
        with open(self.description_path, 'w', encoding=DESCRIPTION_CONFIGS['encoding']) as file:
            file.write(html_content)

    def tearDown(self):
        for path in [self.data_path, self.description_path]:
            if os.path.exists(path):
                os.unlink(path)

    def test_clean_html_text(self):
        with open(self.description_path, 'r', encoding=DESCRIPTION_CONFIGS['encoding']) as file:
            soup = BeautifulSoup(file, DESCRIPTION_CONFIGS['parser'])
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text(separator=' ')

        # Test non-breaking space & weird chars fix
        self.assertIn(DESCRIPTION_CONFIGS['breaking_spaces']['pattern'], text)
        self.assertIn(DESCRIPTION_CONFIGS['weird_characters']['pattern'], text)
        cleaned1 = text\
            .replace(
            DESCRIPTION_CONFIGS['breaking_spaces']['pattern']
            , DESCRIPTION_CONFIGS['breaking_spaces']['repl'])\
            .replace(
            DESCRIPTION_CONFIGS['weird_characters']['pattern']
            , DESCRIPTION_CONFIGS[ 'weird_characters']['repl'])
        self.assertNotIn(DESCRIPTION_CONFIGS['breaking_spaces']['pattern'], cleaned1)
        self.assertNotIn(DESCRIPTION_CONFIGS['weird_characters']['pattern'], cleaned1)

        # Test normalization
        assert (
                re.search(DESCRIPTION_CONFIGS['section_name']['pattern'], cleaned1, re.IGNORECASE) or
                re.search(DESCRIPTION_CONFIGS['sas_variable_name']['pattern'], cleaned1, re.IGNORECASE)
        )
        cleaned2 = re.sub(
            DESCRIPTION_CONFIGS['section_name']['pattern']
            , DESCRIPTION_CONFIGS['section_name']['repl']
            , cleaned1
            , flags=re.IGNORECASE)
        cleaned2 = re.sub(
            DESCRIPTION_CONFIGS['sas_variable_name']['pattern']
            , DESCRIPTION_CONFIGS['sas_variable_name']['repl']
            , cleaned2
            , flags=re.IGNORECASE)
        spaces_sas_after = len(re.findall(r'SAS\s+(?=\w)', cleaned2))
        spaces_var_after = len(re.findall(r'Variable\s+(?=\w)', cleaned2))
        spaces_name_after = len(re.findall(r'Name:\s+(?=\w)', cleaned2))
        spaces_section_after = len(re.findall(r'Section\s+(?=\w)', cleaned2))
        assert spaces_sas_after == 1
        assert spaces_var_after == 1
        assert spaces_name_after == 2 # Do not forget that it counts here for "Section Name: " and "SAS Variable Name: ", so it's 2 # NOQA E501
        assert spaces_section_after == 1

    def test_extract_html_text(self):
        result = extract_html_text(self.description_path)
        expected = "SAS Variable Name: AGE \n Section Name: DEMO \n More text with non-breaking spaces"
        self.assertEqual(result.strip(), expected.strip())

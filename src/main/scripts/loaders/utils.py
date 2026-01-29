from bs4 import BeautifulSoup
import re
from src.main.configs.loaders.data_loader import DESCRIPTION_CONFIGS

def _clean_html_text(text):
    # A quick fix on some exact non-breaking spaces & weird chars
    text = text\
        .replace(
        DESCRIPTION_CONFIGS['breaking_spaces']['pattern']
        , DESCRIPTION_CONFIGS['breaking_spaces']['repl'])\
        .replace(
        DESCRIPTION_CONFIGS['weird_characters']['pattern']
        , DESCRIPTION_CONFIGS['weird_characters']['repl'])
    # A normalization of only the needed section headers
    text = re.sub(
        pattern=DESCRIPTION_CONFIGS['section_name']['pattern']
        , repl=DESCRIPTION_CONFIGS['section_name']['repl']
        , string=text
        , flags=re.IGNORECASE
    )
    text = re.sub(
        pattern=DESCRIPTION_CONFIGS['sas_variable_name']['pattern']
        , repl=DESCRIPTION_CONFIGS['sas_variable_name']['repl']
        , string=text
        , flags=re.IGNORECASE
    )
    return text.strip()

def extract_html_text(html_path):
    with open(html_path, 'r', encoding=DESCRIPTION_CONFIGS['encoding']) as file:
        soup = BeautifulSoup(file, DESCRIPTION_CONFIGS['parser'])
    for script in soup(["script", "style"]):
        script.decompose()
    text = soup.get_text(separator=' ')
    return _clean_html_text(text)
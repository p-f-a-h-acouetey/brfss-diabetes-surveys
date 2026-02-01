import re
import logging
from src.main.configs.cleaners.description_cleaner import DESCRIPTION_CONFIGS


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class DescriptionCleaner:
    def __init__(self, raw_description):
        logger.info("Initializing DescriptionCleaner with your 'raw_description'")
        if len(raw_description.strip()) == 0:
            logger.error("Description is empty from raw_description")
            raise ValueError("Your Description is empty")
        self.raw_description = raw_description.strip()
        self.clean_description = None

    def clean(self):
        logger.info(f"Cleaning your text of {len(self.raw_description)} characters")

        text = self.raw_description
        before_clean = len(text)
        # A quick fix on some exact non-breaking spaces & weird chars
        text = text.replace(
            DESCRIPTION_CONFIGS["breaking_spaces"]["pattern"],
            DESCRIPTION_CONFIGS["breaking_spaces"]["repl"],
        ).replace(
            DESCRIPTION_CONFIGS["weird_characters"]["pattern"],
            DESCRIPTION_CONFIGS["weird_characters"]["repl"],
        )
        # A normalization of only the needed section headers
        text = re.sub(
            pattern=DESCRIPTION_CONFIGS["section_name"]["pattern"],
            repl=DESCRIPTION_CONFIGS["section_name"]["repl"],
            string=text,
            flags=re.IGNORECASE,
        )
        text = re.sub(
            pattern=DESCRIPTION_CONFIGS["sas_variable_name"]["pattern"],
            repl=DESCRIPTION_CONFIGS["sas_variable_name"]["repl"],
            string=text,
            flags=re.IGNORECASE,
        )
        after_clean = len(text)
        self.clean_description = text
        logger.info(
            f"Cleaned your text from {before_clean} to {after_clean} characters"
        )

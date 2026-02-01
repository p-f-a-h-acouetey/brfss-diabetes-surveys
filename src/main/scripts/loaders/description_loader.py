import logging
from bs4 import BeautifulSoup
from src.main.configs.loaders.description_loader import DESCRIPTION_CONFIGS


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class DescriptionLoader:
    def __init__(self, raw_description_path):
        logger.info(
            f"Initializing DescriptionLoader with description_path='{raw_description_path}'"
        )

        if not raw_description_path.endswith(".HTML"):
            logger.error(
                f"Invalid description_path: '{raw_description_path}' - must end in .HTML"
            )
            raise ValueError("Your DescriptionPath must end in .HTML")

        self.raw_description_path = raw_description_path
        self.raw_description = None

        logger.info("DescriptionLoader initialized successfully")

    def read_description(self):
        logger.info(f"Reading HTML description from: {self.raw_description_path}")

        with open(
            self.raw_description_path, "r", encoding=DESCRIPTION_CONFIGS["encoding"]
        ) as file:
            soup = BeautifulSoup(file, DESCRIPTION_CONFIGS["parser"])
        raw_text = soup.get_text(separator=" ")
        logger.debug(f"Raw description length: {len(raw_text)} characters")

        if len(raw_text) == 0:
            logger.error(f"Description is empty from {self.raw_description_path}")
            raise ValueError("Your Description is empty")

        self.raw_description = raw_text
        logger.info(
            f"Description loaded successfully: {len(self.raw_description)} characters"
        )

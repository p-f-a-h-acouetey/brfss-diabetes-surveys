import pyreadstat
import logging
from src.main.configs.loaders.data_loader import DATA_CONFIGS
from src.main.scripts.loaders.utils import extract_html_text


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class DataLoader:
    def __init__(self, data_path, description_path):
        logger.info(
            f"Initializing DataLoader with data_path='{data_path}', description_path='{description_path}'"
        )

        if not data_path.endswith(".xpt"):
            logger.error(f"Invalid data_path: '{data_path}' - must end in .xpt")
            raise ValueError("Your DataPath must end in .xpt")
        if not description_path.endswith(".HTML"):
            logger.error(
                f"Invalid description_path: '{description_path}' - must end in .HTML"
            )
            raise ValueError("Your DescriptionPath must end in .HTML")

        self.data_path = data_path
        self.description_path = description_path
        self.data = None
        self.description = None

        logger.info("DataLoader initialized successfully")

    def _read_data(self):
        logger.info(f"Reading XPT data from: {self.data_path}")

        try:
            df, metadata = pyreadstat.read_xport(
                self.data_path, encoding=DATA_CONFIGS["encoding"]
            )
            logger.debug(f"Raw data loaded: {df.shape[0]} rows, {df.shape[1]} columns")

            if df.empty:
                logger.error(f"DataFrame is empty from {self.data_path}")
                raise ValueError("Your DataFrame contains ZERO row")

            self.data = df.copy()
            logger.info(
                f"Data loaded successfully: {self.data.shape[0]} rows, {self.data.shape[1]} columns"
            )

        except Exception as e:
            logger.error(f"Failed to read XPT file {self.data_path}: {str(e)}")
            raise

    def _read_description(self):
        logger.info(f"Reading HTML description from: {self.description_path}")

        try:
            text = extract_html_text(self.description_path)
            logger.debug(f"Raw description length: {len(text)} characters")

            if len(text) == 0:
                logger.error(f"Description is empty from {self.description_path}")
                raise ValueError("Your Description is empty")

            self.description = text
            logger.info(
                f"Description loaded successfully: {len(self.description)} characters"
            )

        except Exception as e:
            logger.error(
                f"Failed to read description {self.description_path}: {str(e)}"
            )
            raise

    def full_load(self):
        logger.info("Starting full_load() - data + description")

        try:
            self._read_data()
            self._read_description()
            logger.info("full_load() completed successfully")

        except Exception as e:
            logger.error(f"full_load() failed: {str(e)}")
            raise

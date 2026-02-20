import pyreadstat
import loguru
from brfss_diabetes_surveys_etl.src.main.configs.loaders.data_loader import (
    LOADING_CONFIGS,
)

logger = loguru.logger


class DataLoader:
    def __init__(self, raw_data_path: str) -> None:
        logger.info(f"Initializing DataLoader with raw_data_path='{raw_data_path}'")

        if not raw_data_path.endswith(".xpt"):
            raise ValueError("Your raw_data_path must end in .xpt")

        self.raw_data_path = raw_data_path
        self.raw_df = None

        logger.info("DataLoader initialized successfully")

    def read_data(self) -> None:
        logger.info(f"Reading XPT data from: {self.raw_data_path}")

        raw_df, metadata = pyreadstat.read_xport(
            self.raw_data_path, encoding=LOADING_CONFIGS["encoding"]
        )

        if raw_df.empty:
            raise ValueError("Your DataFrame contains ZERO row and ZERO column")

        self.raw_df = raw_df.copy()
        logger.info(
            f"Data loaded successfully: {self.raw_df.shape[0]} rows, {self.raw_df.shape[1]} columns"
        )

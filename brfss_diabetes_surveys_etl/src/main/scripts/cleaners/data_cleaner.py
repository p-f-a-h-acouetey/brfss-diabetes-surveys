import logging
import pandas as pd
from brfss_diabetes_surveys_etl.src.main.configs.cleaners.data_cleaner import (
    CLEANING_CONFIGS,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class DataCleaner:
    def __init__(self, raw_df: pd.DataFrame) -> None:
        logger.info("Initializing DataCleaner with your 'raw_df'")
        if raw_df.empty:
            raise ValueError("Your DataFrame is empty")
        self.df = raw_df.copy()

    def clean_data(self) -> None:
        logger.info("Starting clean_data()")
        num_rows_before = len(self.df)
        num_cols_before = len(self.df.columns)

        logger.info("Reading cleaning configs")
        cols_to_keep = [col for configs in CLEANING_CONFIGS.values() for col in configs]
        df = self.df.copy()[cols_to_keep]

        df = df.drop_duplicates()
        self.df = df.copy()
        num_rows_after = len(self.df)
        num_cols_after = len(self.df.columns)
        logger.info(
            f"clean_data() completed successfully: "
            f"Going from {(num_rows_before, num_cols_before)} "
            f"to {(num_rows_after, num_cols_after)}"
        )

import logging
import pandas as pd
from brfss_diabetes_surveys_etl.src.main.scripts.loaders.data_loader import DataLoader
from brfss_diabetes_surveys_etl.src.main.scripts.cleaners.data_cleaner import (
    DataCleaner,
)
from brfss_diabetes_surveys_etl.src.main.scripts.sinkers.data_sinker import DataSinker


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ETLPipeline:
    def __init__(self, raw_data_path: str) -> None:
        logger.info(f"Initializing ETLPipeline with raw_data_path='{raw_data_path}'")
        if len(raw_data_path.strip()) == 0:
            raise ValueError("Your raw_data_path cannot be empty")
        self.raw_data_path = raw_data_path

    def run(self) -> pd.DataFrame:
        logger.info("Running pipeline")
        data_loader = DataLoader(raw_data_path=self.raw_data_path)
        data_loader.read_data()
        raw_df = data_loader.raw_df.copy()
        data_cleaner = DataCleaner(raw_df=raw_df)
        data_cleaner.clean_data()
        clean_df = data_cleaner.df.copy()
        data_sinker = DataSinker(clean_df=clean_df)
        data_sinker.sink_data()
        logger.info("Successfully completed pipeline")

        return clean_df

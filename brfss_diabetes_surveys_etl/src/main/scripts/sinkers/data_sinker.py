import logging
import pandas as pd
from brfss_diabetes_surveys_etl.src.main.configs.sinkers.data_sinker import SINK_CONFIGS

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class DataSinker:
    def __init__(self, clean_df: pd.DataFrame) -> None:
        logger.info("Initializing DataSinker with your 'clean_df'")
        if clean_df.empty:
            raise ValueError("Your DataFrame is empty")
        self.df = clean_df

    def sink_data(self) -> None:
        logger.info("Starting sink_data()")
        self.df.to_parquet(
            path=f"{SINK_CONFIGS['path']}/LLCP2024{SINK_CONFIGS['format']}",
            index=False,
        )
        logger.info(
            f"sink_data() completed successfully: "
            f"Save data in the path {SINK_CONFIGS['path']}"
        )

import pandas as pd
import loguru
from brfss_diabetes_surveys_ml.src.main.configs.loaders.data_loader import (
    LOADING_CONFIGS,
)

logger = loguru.logger


class DataLoader:
    def __init__(self, data_path: str) -> None:
        logger.info(f"Initializing DataLoader with data_path='{data_path}'")

        if not data_path.endswith(".parquet"):
            raise ValueError("Your raw_data_path must end in .parquet")

        self.data_path = data_path
        self.df = None

        logger.info("DataLoader initialized successfully")

    def read_data(self) -> None:
        logger.info(f"Reading PARQUET data from: {self.data_path}")

        df = pd.read_parquet(self.data_path, engine=LOADING_CONFIGS["engine"])

        if df.empty:
            raise ValueError("Your DataFrame contains ZERO sample and ZERO variable")

        self.df = df.copy()
        logger.info(
            f"Data loaded successfully: {self.df.shape[0]} sample(s), {self.df.shape[1]} variable(s)"
        )

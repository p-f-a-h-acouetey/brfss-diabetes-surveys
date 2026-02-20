import loguru
import numpy as np
import pandas as pd
from brfss_diabetes_surveys_ml.src.main.configs.cleaners.data_cleaner import (
    CLEANING_CONFIGS,
)

logger = loguru.logger


class DataCleaner:
    def __init__(self, df: pd.DataFrame) -> None:
        logger.info("Initializing DataCleaner with your 'df'")
        if df.empty:
            raise ValueError("Your DataFrame is empty")
        self.df = df.copy()

    @staticmethod
    def _apply_cleaning(df: pd.DataFrame, configs: dict) -> pd.DataFrame:
        for col, cfg in configs.items():
            cfg_type = cfg.get("type")
            new_name = cfg["new_name"] if "new_name" in cfg else col

            if cfg_type == "np_select":
                conditions = [eval(expr, {}, {"df": df}) for expr in cfg["conditions"]]
                df[new_name] = np.select(conditions, cfg["choices"], default=None)

            elif cfg_type == "np_where":
                cond = eval(cfg["condition"], {}, {"df": df})
                df[new_name] = np.where(cond, cfg["true_value"], df[col])

            elif cfg_type == "pd_map":
                df[new_name] = df[col].map(cfg["map"])

            elif cfg_type is None:
                df.rename(columns={col: new_name}, inplace=True)

            if "dtypes" in cfg:
                df[new_name] = df[new_name].astype(cfg["dtypes"])

            # Drop original column after successful transformation
            if col in df.columns:
                df.drop(columns=[col], inplace=True)

        return df

    def clean_data(self) -> None:
        logger.info("Starting clean_data()")
        num_rows_before = len(self.df)
        num_cols_before = len(self.df.columns)

        df = self.df.copy()
        clean_df = self._apply_cleaning(df, CLEANING_CONFIGS)

        # Remove unwanted diabetes_categories
        clean_df = clean_df.dropna(subset=["diabetic_status"])

        clean_df = clean_df.drop_duplicates()
        ordered_cols = sorted(list(clean_df.columns))
        clean_df = clean_df[ordered_cols]

        self.df = clean_df.copy()
        num_rows_after = len(self.df)
        num_cols_after = len(self.df.columns)
        logger.info(
            f"clean_data() completed successfully: "
            f"Going from {(num_rows_before, num_cols_before)} "
            f"to {(num_rows_after, num_cols_after)}"
        )

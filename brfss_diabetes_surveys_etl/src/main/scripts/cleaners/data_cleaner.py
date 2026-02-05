import re
import logging
from brfss_diabetes_surveys_etl.src.main.configs.cleaners.data_cleaner import (
    DATA_CONFIGS,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# The process was defined in this way, because we do not know deterministically all the columns we will keep


class DataCleaner:
    def __init__(self, raw_df, clean_description):
        logger.info(
            "Initializing DataCleaner with your 'raw_df' and 'clean_description'"
        )
        if raw_df.empty:
            logger.error("DataFrame is empty from raw_df")
            raise ValueError("Your DataFrame is empty")
        if len(clean_description.strip()) == 0:
            logger.error("Description is empty from clean_description")
            raise ValueError("Your Description is empty")
        self.df = raw_df.copy()
        self.clean_description = clean_description.strip()

    def _ensure_not_empty(self, step_name: str):
        if self.df.empty:
            logger.error(f"DataFrame is empty after {step_name}")
            raise ValueError(f"Your DataFrame contains ZERO row after {step_name}")

    def _remove_bfrss_computed_vars(self):
        df = self.df.copy()
        matches = re.findall(
            DATA_CONFIGS["bfrss_computed_vars"]["pattern"],
            self.clean_description,
            re.DOTALL | re.IGNORECASE,
        )
        cols_to_remove = set(list(matches))
        # Not all these columns are present or will be excluded
        cols_to_remove = [
            col
            for col in cols_to_remove.intersection(df.columns)
            if col not in DATA_CONFIGS["bfrss_computed_vars"]["vars_to_keep"]
        ]
        df = df.drop(columns=cols_to_remove)
        logger.info(
            f"Removed {len(cols_to_remove)} BRFSS computed variables successfully"
        )
        self.df = df.copy()

    def _remove_bfrss_record_identification_vars(self):
        df = self.df.copy()
        matches = re.findall(
            DATA_CONFIGS["bfrss_record_identification_vars"]["pattern"],
            self.clean_description,
            re.DOTALL | re.IGNORECASE,
        )
        cols_to_remove = set(list(matches))
        # Not all these columns are present or will be excluded
        cols_to_remove = [
            col
            for col in cols_to_remove.intersection(df.columns)
            if col
            not in DATA_CONFIGS["bfrss_record_identification_vars"]["vars_to_keep"]
        ]
        df = df.drop(columns=cols_to_remove)
        logger.info(
            f"Removed {len(cols_to_remove)} BRFSS record identification variables successfully"
        )
        self.df = df.copy()

    def _remove_brfss_highly_imbalanced_vars(self):
        df = self.df.copy()
        cols_max_prop = {
            col: df[col].value_counts(normalize=True, dropna=False).iloc[0]
            for col in df.columns
        }
        cols_to_remove = [
            col
            for col in cols_max_prop.keys()
            if cols_max_prop[col]
            >= DATA_CONFIGS["brfss_highly_imbalanced_vars"]["threshold"]
        ]
        logger.info(
            f"Removed {len(cols_to_remove)} variables having an extremely dominant value successfully"
        )
        df = df.drop(columns=cols_to_remove)
        self.df = df.copy()

    def _reorganize_diabetes_vars(self):
        df = self.df.copy()
        diatebes_target_col = DATA_CONFIGS["brfss_diabetes_vars"]["var_to_keep"]

        diabetes_cols = df.filter(
            regex=DATA_CONFIGS["brfss_diabetes_vars"]["pattern"], axis=1
        ).columns.tolist()
        cols_to_remove = [col for col in diabetes_cols if col != diatebes_target_col]
        logger.info(
            f"Removed {len(cols_to_remove)} unwanted 'DIAB' columns successfully"
        )
        df = df.drop(columns=cols_to_remove)

        df[diatebes_target_col] = df[diatebes_target_col].replace(
            DATA_CONFIGS["brfss_diabetes_vars"]["values_map"]
        )
        df = df[
            df[diatebes_target_col].isin(
                DATA_CONFIGS["brfss_diabetes_vars"]["values_to_keep"]
            )
        ]

        logger.info(
            f"Reorganized {DATA_CONFIGS['brfss_diabetes_vars']['var_to_keep']} column successfully"
        )
        self.df = df.copy()

    def _detect_brfss_categorical_vars(self):
        df = self.df.copy()
        cat_cols = [
            col
            for col in df.columns
            if df[col].nunique() <= DATA_CONFIGS["brfss_categorical_vars"]["threshold"]
        ]

        logger.info(f"Encoded {len(cat_cols)} variables as categorical successfully")
        df[cat_cols] = df[cat_cols].astype("category")
        self.df = df.copy()

    def _remove_brfss_vars_with_missing_values(self):
        df = self.df.copy()
        cols_na_prop = {col: df[col].isnull().sum() / len(df) for col in df.columns}
        cols_to_remove = [
            col
            for col in cols_na_prop.keys()
            if cols_na_prop[col]
            >= DATA_CONFIGS["brfss_vars_with_missing_values"]["threshold"]
        ]

        logger.info(
            f"Removed {len(cols_to_remove)} columns with missing values successfully"
        )
        df = df.drop(columns=cols_to_remove)
        self.df = df.copy()

    def _drop_duplicates_rows(self):
        df = self.df.copy()
        num_rows_before = len(df)
        df = df.drop_duplicates()
        num_rows_after = len(df)

        logger.info(
            f"Dropped {num_rows_before - num_rows_after} rows for deduplication successfully"
        )
        self.df = df.copy()

    def clean(self):
        logger.info("Starting clean()")
        num_rows_before = len(self.df)
        num_cols_before = len(self.df.columns)

        self._remove_bfrss_computed_vars()
        self._ensure_not_empty("_remove_bfrss_computed_vars")

        self._remove_bfrss_record_identification_vars()
        self._ensure_not_empty("_remove_bfrss_record_identification_vars")

        self._remove_brfss_highly_imbalanced_vars()
        self._ensure_not_empty("_remove_brfss_highly_imbalanced_vars")

        self._reorganize_diabetes_vars()
        self._ensure_not_empty("_reorganize_diabetes_vars")

        self._detect_brfss_categorical_vars()
        self._ensure_not_empty("_detect_brfss_categorical_vars")

        self._remove_brfss_vars_with_missing_values()
        self._ensure_not_empty("_remove_brfss_vars_with_missing_values")

        self._drop_duplicates_rows()
        self._ensure_not_empty("_drop_duplicates_rows")

        num_rows_after = len(self.df)
        num_cols_after = len(self.df.columns)
        logger.info(
            f"clean() completed successfully: "
            f"Going from {(num_rows_before, num_cols_before)} "
            f"to {(num_rows_after, num_cols_after)}"
        )

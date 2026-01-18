import pandas as pd
import logging
from src.main.configs.loaders.data_loader import SURVEYS_DATA_TYPES

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(message)s", force=True
)


class SurveyLoader:
    """
    Loads and validates survey Parquet data with enforced column types.

    Ensures:
    - File is valid Parquet format
    - All required columns exist
    - Data types match predefined schema
    """

    def __init__(self, data_path: str):
        """
        Initialize SurveyLoader with Parquet file path validation.

        Args:
            data_path: Path to .parquet file containing survey data

        Raises:
            ValueError: If file doesn't end with .parquet extension
        """
        if not data_path.endswith(".parquet"):
            raise ValueError(
                " Invalid file format! Expected a path ending with .parquet"
            )
        self.data_path = data_path
        self.logger = logging.getLogger(__name__)

    def load_df(self) -> pd.DataFrame:
        """
        Load Parquet data with comprehensive validation and type enforcement.

        Steps:
        1. Read Parquet file
        2. Validate required columns exist
        3. Keep only required columns to match schema
        4. Apply strict data types from SURVEYS_DATA_TYPES

        Returns:
            Clean DataFrame with validated schema and optimized dtypes

        Raises:
            ValueError: Missing required columns
        """
        logging.info(f"Loading survey data from: {self.data_path}")
        df = pd.read_parquet(self.data_path)

        required_cols = set(SURVEYS_DATA_TYPES.keys())
        missing_cols = required_cols - set(df.columns)

        if missing_cols:
            raise ValueError(f"Missing cols: {missing_cols}")

        df = df[sorted(required_cols)]
        self.logger.info("Enforcing data types...")
        for col_name, target_dtype in SURVEYS_DATA_TYPES.items():
            if col_name in df.columns:
                current_dtype = df[col_name].dtype
                df[col_name] = df[col_name].astype(target_dtype)
                self.logger.info(f"{col_name}: {current_dtype} → {target_dtype}")

        self.logger.info(f"Loaded {len(df)} rows with validated schema")
        return df

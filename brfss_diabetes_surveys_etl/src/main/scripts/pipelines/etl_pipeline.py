import logging
from brfss_diabetes_surveys_etl.src.main.scripts.cleaners.description_cleaner import (
    DescriptionCleaner,
)
from brfss_diabetes_surveys_etl.src.main.scripts.loaders.description_loader import (
    DescriptionLoader,
)
from brfss_diabetes_surveys_etl.src.main.scripts.cleaners.data_cleaner import (
    DataCleaner,
)
from brfss_diabetes_surveys_etl.src.main.scripts.loaders.data_loader import DataLoader


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ETLPipeline:
    def __init__(self, raw_data_path, raw_description_path):
        logger.info(
            f"Initializing ETLPipeline with raw_data_path='{raw_data_path}' and raw_description_path='{raw_description_path}'"
        )

        if len(raw_data_path.strip()) == 0 or len(raw_description_path.strip()) == 0:
            raise ValueError(
                "Your raw_data_path and raw_description_path cannot be empty"
            )

        self.raw_data_path = raw_data_path
        self.raw_description_path = raw_description_path

    def execute(self):
        logger.info("Running pipeline")
        # Description
        description_loader = DescriptionLoader(
            raw_description_path=self.raw_description_path
        )
        description_loader.read_description()
        description_cleaner = DescriptionCleaner(
            raw_description=description_loader.raw_description
        )
        description_cleaner.clean()
        # Data
        data_loader = DataLoader(raw_data_path=self.raw_data_path)
        data_loader.read_data()
        data_cleaner = DataCleaner(
            raw_df=data_loader.raw_df,
            clean_description=description_cleaner.clean_description,
        )
        data_cleaner.clean()

        return data_cleaner.df

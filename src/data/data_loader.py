import requests
import json
import pandas as pd
from src.utils.logger import get_logger
from src.utils.config import get_config

class BikeDataLoader:
    def __init__(self):
        self.config = get_config()
        self.logger = get_logger("load-data-and-change-data-to-DataFrame")
        self.url = self.config.DATAURL

    def load_data(self) -> json:
        self.logger.info("Loading the bikes data...")
        try:
            response = requests.get(self.url)
            bikes = json.loads(response.text)
            self.logger.info("Data loaded successfully.")
            return bikes
        except Exception as e:
            self.logger.error(f"Error loading data: {e}")

    def json_data_to_dataframe(self, bikes_json: json = None) -> pd.DataFrame:
        self.logger.info("Converting JSON bikes data to a pandas DataFrame...")
        try:
            if bikes_json is None:
                bikes_json = self.load_data()
            bikes_df = pd.DataFrame(bikes_json)
            self.logger.info("Data successfully converted to a DataFrame.")
            return bikes_df
        except Exception as e:
            self.logger.error(f"Error converting JSON data to DataFrame: {e}")


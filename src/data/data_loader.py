import requests
import json
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

from src.utils.logger import get_logger
from src.utils.config import get_config

config = get_config()
logger = get_logger("load-data-and-change-data-to-DataFrame")
url = config.DATAURL

def data() -> json:
    logger.info("Load the bikes data...")
    try:
        response = requests.get(url)
        bikes = json.loads(response.text)
        logger.info("Data loaded successfully.")
        return bikes
    except Exception as e:
        logger.error(f"Error loading data: {e}")


def json_data_to_dataframe(bikes_json: json = data()) -> pd.DataFrame:
    logger.info("Change the json bikes data to a pandas DataFrame...")
    try:
        bikes_df = pd.DataFrame(bikes_json)
        logger.info("Data successfully changed into a DataFrame.")
        return bikes_df
    except Exception as e:
        logger.error(f"Error changing JSON-data to DataFrame: {e}")


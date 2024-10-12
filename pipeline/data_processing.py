import os
import requests
import json
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

# load the bikes data
def data() -> json:
    url = os.getenv('DATAURL')
    response = requests.get(url)
    bikes = json.loads(response.text)
    return bikes


# change the json bikes data to a pandas DataFrame
def json_data_to_dataframe(bikes_json: json = data()) -> pd.DataFrame:
    bikes_df = pd.DataFrame(bikes_json)
    return bikes_df













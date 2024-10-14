# Unit tests for the data loading module
import unittest
import json
from pathlib import Path
import pandas as pd
from unittest.mock import patch, MagicMock
from src.data.data_loader import BikeDataLoader
from src.utils.logger import get_logger


class TestDataLoader(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # No need to pass self explicitly
        self.logger = get_logger("Unit testing for the data loading module...")

    def setUp(self):
        self.logger.info("Correctly construct the relative path to the bikes JSON data.")
        json_path = Path(__file__).parent.parent / 'data' / 'bikes_data.json'

        self.logger.info("Load the expected JSON data from the file...")
        with open(json_path, 'r') as json_file:
            self.expected_json_data = json.load(json_file)

        self.logger.info("Load expected csv DataFrame (Not needed for similarity search though)")
        csv_path = Path(__file__).parent.parent / 'data' / 'bikes_data.csv'
        self.expected_dataframe = pd.read_csv(csv_path)


    @patch('src.data.data_loader.requests.get')
    def test_data_loader_with_file(self, mock_get):
        self.logger.info("Simulate the API response")
        mock_response = MagicMock()
        self.logger.info("Convert expected JSON to string format.")
        mock_response.text = json.dumps(self.expected_json_data)
        mock_get.return_value = mock_response

        self.logger.info("Call the data function")
        result = BikeDataLoader().load_data()

        self.logger.info("Assert that the result from the API matches the expected JSON data")
        self.assertEqual(result, self.expected_json_data)

    @patch('src.data.data_loader.pd.DataFrame')
    def test_json_data_to_dataframe_with_file(self, mock_dataframe):
        self.logger.info("Set the mock DataFrame to return the expected DataFrame")
        mock_dataframe.return_value = self.expected_dataframe

        self.logger.info("Call the json_data_to_dataframe function")
        result = BikeDataLoader().json_data_to_dataframe(self.expected_json_data)

        self.logger.info("Assert that the DataFrame was called with the correct JSON data")
        mock_dataframe.assert_called_once_with(self.expected_json_data)

        self.logger.info("Compare the result with the expected DataFrame")
        pd.testing.assert_frame_equal(result, self.expected_dataframe)


if __name__ == '__main__':
    unittest.main()


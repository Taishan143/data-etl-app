import unittest
from spotify_data_etl.extract.base_api import BaseAPIExtract
from spotify_data_etl.config.base_config import parse_yaml_config
import yaml
import pandas as pd


class MockBaseAPIExtract(BaseAPIExtract):
    """The CSVDataCleanser is an abstract class and cannot be instantiated.
    This is a test sub class used for testing the DataCleanser methods which are not abstract.
    """

    def authenticate(self):
        """Mock implementation for testing purposes."""
        # Return nothing.
        return None

    def extract_data(self) -> pd.DataFrame:
        """Mock implementation for testing purposes."""
        # return an empty dataframe for simplicity.
        return pd.DataFrame({})


class TestBaseApi(unittest.TestCase):

    def setUp(self):
        test_config_path = "tests/test_data/test-config.yaml"
        with open(test_config_path, "r") as file:
            self.config_data = yaml.safe_load(file)

        self.config = parse_yaml_config(config_data=self.config_data)

    def test_validate_data_size(self):
        # Arrange
        test_data = {"test_col": [1, 2, 3], "test_col_2": ["a", "b", "c"]}
        test_dataframe = pd.DataFrame(test_data)
        # Act
        base_api_extract = MockBaseAPIExtract(config=self.config)
        result = base_api_extract.validate_data_size(dataframe=test_dataframe)
        # Assert
        self.assertEqual(result, None)

    def test_validate_data_size__error_raised(self):
        # Arrange
        test_data = {"test_col": [], "test_col_2": []}
        test_dataframe = pd.DataFrame(test_data)
        # Act
        base_api_extract = MockBaseAPIExtract(config=self.config)
        with self.assertRaises(Exception) as context:
            base_api_extract.validate_data_size(dataframe=test_dataframe)
        # Assert
        self.assertIn("No data to process.", str(context.exception))

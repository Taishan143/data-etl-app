import unittest
from unittest.mock import patch, MagicMock
from data_etl_app.extract.apis.kaggle_extract import KaggleExtract
from data_etl_app.config.base_config import parse_yaml_config
import yaml
import pandas as pd
import io
import zipfile
import base64
import os


class TestKaggleExtract(unittest.TestCase):

    def setUp(self):
        test_config_path = "tests/test_data/test-config.yaml"
        with open(test_config_path, "r") as file:
            self.config_data = yaml.safe_load(file)

        self.config = parse_yaml_config(config_data=self.config_data)

    @patch("os.environ", {})
    @patch("data_etl_app.extract.apis.kaggle_extract.KaggleApi")
    def test_authenticate(self, mock_kaggle_api):
        # Arrange
        mock_api_instance = MagicMock()
        mock_kaggle_api.return_value = mock_api_instance

        # Setup environment variables to simulate dotenv loading
        with patch.dict(
            os.environ,
            {"BASIC_KAGGLE_USERNAME": "test_user", "BASIC_KAGGLE_KEY": "test_key"},
        ):
            # Instantiate KaggleAPI with a dummy config object
            dummy_config = MagicMock()
            kaggle_api = KaggleExtract(config=dummy_config)

            # Act
            kaggle_api.authenticate()

            # Assert environment variables are set by authenticate()
            self.assertEqual(os.environ["KAGGLE_USERNAME"], "test_user")
            self.assertEqual(os.environ["KAGGLE_KEY"], "test_key")

            # Assert the authenticate method on the KaggleApi instance was called once
            mock_api_instance.authenticate.assert_called_once()

    @patch("data_etl_app.extract.apis.kaggle_extract.requests.get")
    @patch("data_etl_app.extract.apis.kaggle_extract.zipfile.ZipFile")
    def test_extract_data(self, mock_zipfile_class, mock_requests_get):
        # Arrange
        config_mock = MagicMock()
        config_mock.api.version = "1"
        config_mock.base.base_url = "https://fake-url.com"
        config_mock.base.endpoint = "datasets/download"
        config_mock.api.owner = "ownername"
        config_mock.api.dataset = "datasetname"

        kaggle_api_instance = KaggleExtract(config=config_mock)
        kaggle_api_instance.USERNAME = "user"
        kaggle_api_instance.KEY = "key"

        # Mock the requests.get response
        fake_csv_content = "col1,col2\nval1,val2\nval3,val4"
        fake_csv_bytes = fake_csv_content.encode("utf-8")

        # Create a fake ZIP file in memory containing the CSV
        fake_zip_bytes = io.BytesIO()
        with zipfile.ZipFile(fake_zip_bytes, mode="w") as zf:
            zf.writestr("netflix_titles.csv", fake_csv_bytes)
        fake_zip_bytes.seek(0)

        mock_response = MagicMock()
        mock_response.content = fake_zip_bytes.read()
        mock_requests_get.return_value = mock_response

        # Mock ZipFile to use the in-memory bytes instead of a real file
        mock_zipfile_instance = MagicMock()
        mock_zipfile_instance.open.return_value = io.StringIO(fake_csv_content)
        mock_zipfile_class.return_value = mock_zipfile_instance

        # Act
        result_df = kaggle_api_instance.extract_data()

        # Assert
        expected_df = pd.read_csv(io.StringIO(fake_csv_content), engine="python")
        pd.testing.assert_frame_equal(result_df, expected_df)

        # Verify URL and headers
        expected_url = (
            f"{config_mock.base.base_url}/"
            f"{config_mock.base.endpoint}/"
            f"{config_mock.api.owner}/"
            f"{config_mock.api.dataset}"
            f"?datasetVersionNumber={config_mock.api.version}"
        )
        expected_auth = base64.b64encode(
            bytes(
                f"{kaggle_api_instance.USERNAME}:{kaggle_api_instance.KEY}",
                "ISO-8859-1",
            )
        ).decode("ascii")

        mock_requests_get.assert_called_once_with(
            url=expected_url, headers={"Authorization": f"Basic {expected_auth}"}
        )

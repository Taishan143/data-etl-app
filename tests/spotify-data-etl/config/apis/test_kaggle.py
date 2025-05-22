import unittest
import yaml
from spotify_data_etl.config.apis.kaggle import parse_kaggle_config


class TestKaggleConfig(unittest.TestCase):

    def setUp(self):
        test_config_path = "tests/test_data/test-config.yaml"
        with open(test_config_path, "r") as file:
            self.config_data = yaml.safe_load(file)

    def test_parse_kaggle_config__success(self):
        # Arrange
        # Act
        result = parse_kaggle_config(config_data=self.config_data)
        # Assert
        self.assertEqual(result.owner, "some-owner")
        self.assertEqual(result.dataset, "some-dataset")
        self.assertEqual(result.version, "1")

    def test_parse_kaggle_config__failure(self):
        # Arrange
        config_copy = self.config_data.copy()
        del config_copy["api"]["owner"]
        # Act
        with self.assertRaises(KeyError) as context:
            parse_kaggle_config(config_data=self.config_data)
        # Assert
        self.assertIn("Missing required config key: 'owner'", str(context.exception))

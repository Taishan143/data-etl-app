import unittest
import yaml
from data_etl_app.config.base_config import parse_yaml_config, parse_base_config


class TestBaseConfig(unittest.TestCase):

    def setUp(self):
        test_config_path = "tests/test_data/test-config.yaml"
        with open(test_config_path, "r") as file:
            self.config_data = yaml.safe_load(file)

    def test_parse_yaml_config__success(self):
        # Arrange
        # Act
        result = parse_yaml_config(config_data=self.config_data)
        # Assert
        self.assertEqual(result.base.api, "kaggle")

    def test_parse_yaml_config__failure(self):
        # Arrange
        config_copy = self.config_data.copy()
        config_copy["base"]["api"] = "test"
        # Act
        with self.assertRaises(ValueError) as context:
            parse_yaml_config(config_data=self.config_data)
        # Assert
        self.assertIn("Unsupported API type: test", str(context.exception))

    def test_parse_base_config__success(self):
        # Arrange
        # Act
        result = parse_base_config(config_data=self.config_data)
        # Assert
        self.assertEqual(result.api, "kaggle")

    def test_parse_base_config__failure(self):
        # Arrange
        config_copy = self.config_data.copy()
        del config_copy["base"]["api"]
        # Act
        with self.assertRaises(KeyError) as context:
            parse_base_config(config_data=self.config_data)
        # Assert
        self.assertIn("Missing required base config key: 'api'", str(context.exception))

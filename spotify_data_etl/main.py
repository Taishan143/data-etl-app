from spotify_data_etl.extract.apis.kaggle_api import KaggleAPI
from spotify_data_etl.config.base_config import Config, parse_yaml_config
import yaml
import logging


def main():
    config_data = load_yaml_config(config_filepath="kaggle-config.yaml")
    config: Config = parse_yaml_config(config_data=config_data)
    api_name = config.base.api

    logging.info("Retrieving API client")
    api_client = get_api_client(api_name=api_name)
    api_client_instance = api_client(config=config)

    logging.info(f"authenticating to the {api_name} api...")
    api_client_instance.authenticate()

    logging.info(f"Extracting data from the {api_name} api...")
    extraceted_data = api_client_instance.extract_data()

    api_client_instance.validate_data_size(dataframe=extraceted_data)


def get_api_client(api_name: str):
    apis = {"kaggle": KaggleAPI}

    try:
        return apis[api_name.lower()]
    except KeyError:
        raise ValueError(f"Unsupported API: {api_name}")


def load_yaml_config(config_filepath: str):
    with open(config_filepath, "r") as file:
        return yaml.safe_load(file)

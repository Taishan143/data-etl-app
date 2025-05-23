from data_etl_app.extract.extract_factory import get_extractor_instance, Extractor
from data_etl_app.cleanse.cleanse_factory import get_cleanser_instance, Cleanser
from data_etl_app.transform.transform_factory import (
    get_transformer_instance,
    Transformer,
)
from data_etl_app.load.load_factory import get_loader_instance, Loader
from data_etl_app.visualisations.visualisation_factory import (
    get_visualisation_instance,
    Visualiser,
)
from data_etl_app.config.base_config import Config, parse_yaml_config
import yaml
import logging
import pandas as pd
import sys


# config_file = "kaggle-config.yaml"


def main(config_file: str):
    config_data = load_yaml_config(config_filepath=config_file)
    config: Config = parse_yaml_config(config_data=config_data)
    api_name = config.base.api
    database_name = config.base.database_source

    # Extract the data
    logging.info("Retrieving API client")
    extract_client = get_extractor_instance(api_name=api_name)
    extract_instance: Extractor = extract_client(config=config)

    logging.info(f"authenticating to the {api_name} api...")
    extract_instance.authenticate()

    logging.info(f"Extracting data from the {api_name} api...")
    extraceted_data: pd.DataFrame = extract_instance.extract_data()

    logging.info("Running data validations")
    extract_instance.validate_data_size(dataframe=extraceted_data)

    # Perform cleansing operations
    cleansing_client = get_cleanser_instance(api_name=api_name)
    cleansing_instance: Cleanser = cleansing_client()

    logging.info("Cleaning data...")
    cleansed_data = cleansing_instance.cleanse_data(dataframe=extraceted_data)

    # Transform the data
    transformer_client = get_transformer_instance(api_name=api_name)
    transformer_instance: Transformer = transformer_client()

    transformed_data = transformer_instance.run_transformations(dataframe=cleansed_data)

    logging.info(f"Transformed data (first 10 rows): {transformed_data.head(10)}")

    # Load the data
    loader_client = get_loader_instance(database_name=database_name)
    loader_instance: Loader = loader_client(config=config)

    loader_instance.load_data(dataframe=transformed_data)
    # Visualise data

    connection = loader_instance.create_connection()
    vis_client = get_visualisation_instance(api_name=api_name)
    vis_instance: Visualiser = vis_client(config=config)

    query = f"SELECT * FROM {config.database.table}"
    dataframe = vis_instance.get_data(query=query, connection=connection)
    plot_columns = ("release_year", "diversity_score")
    vis_instance.plot_data(dataframe=dataframe, columns=plot_columns)


def load_yaml_config(config_filepath: str):
    with open(config_filepath, "r") as file:
        return yaml.safe_load(file)


if __name__ == "__main__"():
    main(sys.argv[1])

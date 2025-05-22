from abc import ABC, abstractmethod
from spotify_data_etl.config.base_config import Config
from pandas import DataFrame
import logging


class BaseAPIExtract(ABC):

    def __init__(self, config: Config):
        self.config = config

    @abstractmethod
    def authenticate(self):
        """Overwritten in child classes."""

    @abstractmethod
    def extract_data(self):
        """Overwritten in child classes."""

    def validate_data_size(self, dataframe: DataFrame):
        """Checks to see if any data has been returned.

        :param dataframe: The data extracted from the API.
        :type dataframe: DataFrame
        :raises Exception: Raised if no data is present in the dataframe.
        """
        if dataframe.empty:
            logging.warning("The dataframe contains no data points.")
            raise Exception("No data to process.")

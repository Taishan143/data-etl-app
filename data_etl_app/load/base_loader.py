from abc import ABC, abstractmethod
from data_etl_app.config.base_config import Config


class BaseLoader(ABC):

    def __init__(self, config: Config):
        self.config = config

    @abstractmethod
    def load_data(self):
        """To be implemented by child classes."""

from abc import ABC, abstractmethod
from data_etl_app.config.base_config import Config


class BaseVisualiser(ABC):

    def __init__(self, config: Config):
        self.config = config

    @abstractmethod
    def get_data(self):
        """Override and implement at a  child class level."""
        pass

    @abstractmethod
    def plot_data(self):
        """Override and implement at a  child class level."""
        pass

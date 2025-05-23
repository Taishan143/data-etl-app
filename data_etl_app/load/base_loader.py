from abc import ABC, abstractmethod


class BaseLoader(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def load_data(self):
        """To be implemented by child classes."""

from abc import ABC, abstractmethod


class BaseTransformer(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def run_transformations(self):
        """To be implemented by child classes."""

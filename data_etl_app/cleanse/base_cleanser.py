from abc import ABC, abstractmethod


class BaseCleanser(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def cleanse_data(self):
        """Instantiate at a child class level"""

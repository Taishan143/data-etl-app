from abc import ABC, abstractmethod


class BaseVisualiser(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def plot_data(self):
        pass

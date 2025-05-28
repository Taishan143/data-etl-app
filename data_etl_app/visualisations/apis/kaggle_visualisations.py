from data_etl_app.visualisations.base_visualisations import BaseVisualiser
from data_etl_app.config.base_config import Config
import pandas as pd
from typing import Tuple
from dotenv import load_dotenv
import os
from mysql.connector.pooling import PooledMySQLConnection
from mysql.connector.abstracts import MySQLConnectionAbstract
import matplotlib.pyplot as plt


class KaggleVisualisations(BaseVisualiser):

    def __init__(self, config: Config):
        super().__init__(config=config)
        self.config = config

        load_dotenv()
        self.host = "localhost"
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")

    def get_data(
        self, query: str, connection: PooledMySQLConnection | MySQLConnectionAbstract
    ):
        dataframe = pd.read_sql(query, connection)
        connection.close()

        return dataframe

    def plot_data(
        self,
        dataframe: pd.DataFrame,
        columns: Tuple[str, str],
        title: str,
        xlabel: str,
        ylabel: str,
    ):
        """Plot a basic scatter plot for 2 columns in the dataframe.

        :param dataframe: The data to be plotted.
        :type dataframe: pd.DataFrame
        :param columns: The two columns who's data will be plotted.
        :type columns: Tuple[str, str]
        :param title: The title of the graph.
        :type title: str
        :param xlabel: The label for the x axis.
        :type xlabel: str
        :param ylabel: The label for the y axis.
        :type ylabel: str
        """
        column1, column2 = columns
        x = dataframe[column1]
        y = dataframe[column2]

        plt.figure(figsize=(12, 6))
        plt.bar(x, y, color="skyblue")
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        unique_x_labels = sorted(set(x))
        plt.xticks(unique_x_labels, rotation=45, ha="right")

        plt.tight_layout()
        plt.show()

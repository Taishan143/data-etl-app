from data_etl_app.load.base_loader import BaseLoader
from data_etl_app.config.base_config import Config
import pandas as pd
from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector.cursor import MySQLCursorAbstract
from mysql.connector import Error
import logging


class MySQLLoader(BaseLoader):

    def __init__(self, config: Config):
        super().__init__(config=config)
        self.config = config

        load_dotenv()
        self.host = "localhost"
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")

    def create_connection(self):
        """Establishes a connection to MySQL.

        :raises e: Raised if the connection is refused.
        :return: A connection used for executing queries.
        :rtype: ```(PooledMySQLConnection | MySQLConnectionAbstract)```
        """
        try:
            return mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.config.database.name,
            )
        except Error as e:
            logging.error(f"An error occurred: {e}")
            raise e

    def create_table(self, cursor: MySQLCursorAbstract):
        """Create a table in the database

        :param cursor: Connection cursor used for executing queries.
        :type cursor: MySQLCursorAbstract
        """
        cursor.execute(
            self.config.database.queries["create"].format(
                table=self.config.database.table
            )
        )

    def insert_data(self, cursor: MySQLCursorAbstract, dataframe: pd.DataFrame):
        """Insert data into a table.

        :param cursor: Connection cursor used for executing queries.
        :type cursor: MySQLCursorAbstract
        :param dataframe: The data to be imnserted
        :type dataframe: pd.DataFrame
        """
        columns = list(dataframe.columns)
        placeholders = ", ".join(["%s"] * len(columns))

        update_cols = [col for col in columns if col != "show_id"]
        update_expr = ", ".join([f"{col}=VALUES({col})" for col in update_cols])

        query = (
            f"INSERT INTO {self.config.database.table} ({', '.join(columns)}) VALUES ({placeholders})"
            f"ON DUPLICATE KEY UPDATE {update_expr}"
        )

        data_tuples = [tuple(nparray) for nparray in dataframe.to_numpy()]

        cursor.executemany(query, data_tuples)

    def show_data(self, cursor: MySQLCursorAbstract):
        """Show the data inside the database.

        :param cursor: Connection cursor used for executing queries.
        :type cursor: MySQLCursorAbstract
        """
        cursor.execute(f"SELECT * FROM {self.config.database.table}")

    def load_data(self, dataframe: pd.DataFrame):

        if self.config.database.name == "":
            logging.info("No table name declared. Skipping upload.")
        else:
            connection = self.create_connection()
            cursor = connection.cursor()

            logging.info(
                f"Creating table {self.config.database.table} if it doesn't exist."
            )
            self.create_table(cursor=cursor)
            logging.info("Inserting data...")
            self.insert_data(cursor=cursor, dataframe=dataframe)
            logging.info(
                f"Data successfully inserted into the {self.config.database.table} table."
            )
            self.show_data(cursor=cursor)

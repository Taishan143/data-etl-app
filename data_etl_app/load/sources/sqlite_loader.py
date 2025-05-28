from data_etl_app.load.base_loader import BaseLoader
from data_etl_app.config.base_config import Config
import pandas as pd
import sqlite3
from sqlite3 import Cursor, Connection
import logging


class SQLliteLoader(BaseLoader):

    def __init__(self, config: Config):
        super().__init__(config=config)

    def create_connection(self):
        """Establishes a connection to MySQL.

        :raises e: Raised if the connection is refused.
        :return: A connection used for executing queries.
        :rtype: ```sqlite3.Cursor```
        """
        try:
            return sqlite3.connect(
                database=self.config.database.name,
            )
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            raise e

    def create_table(self, cursor: Cursor):
        """Create a table in the database

        :param cursor: Connection cursor used for executing queries.
        :type cursor: sqlite3.Cursor
        """
        cursor.execute(
            self.config.database.queries["create"].format(
                table=self.config.database.table
            )
        )

    def insert_data(self, connection: Connection, dataframe: pd.DataFrame):
        """Insert data into a table.

        :param connection: Connection used for executing queries.
        :type connection: sqlite3.Connection
        :param dataframe: The data to be imnserted
        :type dataframe: pd.DataFrame

        TODO: Add logic to update dataframes. Currently, the dataframe is replaced.
        """
        dataframe.to_sql(
            self.config.database.table, connection, if_exists="replace", index=False
        )

    def show_data(self, cursor: Cursor):
        """Show the data inside the database.

        :param cursor: Connection cursor used for executing queries.
        :type cursor: MySQLCursorAbstract
        """
        cursor.execute(f"SELECT * FROM {self.config.database.table}")
        cursor.fetchall()

    def load_data(self, dataframe: pd.DataFrame):

        if self.config.database.name == "":
            logging.info("No database declared. Skipping upload.")
        else:
            connection = self.create_connection()
            cursor = connection.cursor()

            logging.info(
                f"Creating table {self.config.database.table} if it doesn't exist."
            )
            self.create_table(cursor=cursor)
            logging.info("Inserting data...")
            self.insert_data(connection=connection, dataframe=dataframe)
            connection.commit()
            logging.info(
                f"Data successfully inserted into the {self.config.database.table} table."
            )
            self.show_data(cursor=cursor)

            cursor.close()
            connection.close()

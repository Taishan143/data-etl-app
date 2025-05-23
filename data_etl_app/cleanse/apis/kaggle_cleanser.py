from data_etl_app.cleanse.base_cleanser import BaseCleanser
import pandas as pd
from typing import Union
from datetime import datetime
import logging


class KaggleDataCleanser(BaseCleanser):

    def __init__(self):
        super().__init__()

    def reformat_date(self, date_str: str) -> str | None:
        """Reformats a date string into a more readable format for data analysis.

        :param date_str: The date as a string.
        :type date_str: str
        :return: The reformatted date in YYYY-mm-dd format.
        :rtype: ```str```
        """
        if pd.isna(date_str):
            logging.warning("Null date object detected.")
            return None
        else:
            try:
                return datetime.strptime(date_str, "%B %d, %Y").strftime("%Y-%m-%d")
            except Exception as e:
                logging.warning(f"Failed to parse date: {date_str}. Error: {e}")
                return None

    def populate_null_values(
        self, dataframe: pd.DataFrame, column: str, value: Union[str, int]
    ):
        """Populates null values withing a dataframe series with a specified value.

        :param dataframe: The dataframe being cleansed.
        :type dataframe: pd.DataFrame
        :param column: The column who's null values we will populate.
        :type column: str
        :param value: The value being inserted into the null fields.
        :type value: Union[str, int]
        """
        dataframe[column].fillna(value, inplace=True)

    def cleanse_data(self, dataframe: pd.DataFrame):
        """Main cleansing operation for the Kaggle API. Method override from the parent class.

        :param dataframe: The dataframe being cleansed.
        :type dataframe: pd.DataFrame
        :return: The cleansed dataframe.
        :rtype: ```pd.DataFrame```
        """
        dataframe["date_added"] = dataframe["date_added"].apply(self.reformat_date)
        columns_and_values = [
            ("director", "Unknown"),
            ("cast", "Unknown"),
            ("country", "Unknown"),
        ]
        for column, value in columns_and_values:
            self.populate_null_values(dataframe=dataframe, column=column, value=value)

        return dataframe

from data_etl_app.transform.base_transformer import BaseTransformer
import pandas as pd
import numpy as np
import logging


class KaggleTransformer(BaseTransformer):

    def __init__(self):
        super().__init__()

    def convert_movie_times_to_hours_and_minutes(self, time_value: str):
        if time_value is pd.NA or time_value is np.nan:
            return "Unknown"
        else:
            try:
                cleansed_time_value = int(time_value.replace("min", ""))
                hours = cleansed_time_value // 60
                minutes = cleansed_time_value % 60
                return f"{hours}h {minutes}m"
            except AttributeError as aterr:
                logging.warning(f"Unparsable duration {time_value}, Error: {aterr}")

    def create_diversity_column(self, dataframe: pd.DataFrame):
        dataframe["diversity_score"] = dataframe["listed_in"].apply(
            lambda col: len(col.split(",")) if isinstance(col, str) else 0
        )
        return dataframe

    def create_adults_only_column(self, dataframe: pd.DataFrame):
        dataframe["adults_only"] = (
            dataframe["rating"].isin(["R", "TV-MA"]).map({True: "Yes", False: "No"})
        )
        return dataframe

    def run_transformations(self, dataframe: pd.DataFrame):

        dataframe.loc[dataframe["type"] == "Movie", "duration"] = dataframe.loc[
            dataframe["type"] == "Movie", "duration"
        ].apply(self.convert_movie_times_to_hours_and_minutes)

        dataframe = self.create_diversity_column(dataframe=dataframe)

        cleansed_dataframe = self.create_adults_only_column(dataframe=dataframe)

        return cleansed_dataframe

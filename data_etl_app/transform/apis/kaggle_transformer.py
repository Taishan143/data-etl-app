from data_etl_app.transform.base_transformer import BaseTransformer
import pandas as pd


class KaggleTransformer(BaseTransformer):

    def __init__(self):
        super().__init__()

    def convert_movie_times_to_hours_and_minutes(self, time_value: str):
        cleansed_time_value = int(time_value.replace("min", ""))
        hours = cleansed_time_value // 60
        minutes = cleansed_time_value % 60

        return f"{hours}h {minutes}m"

    def create_diversity_column(self, dataframe: pd.DataFrame):
        dataframe["diversity_score"] = dataframe["listed_in"].apply(
            lambda col: len(col.split(",")) if isinstance(col, str) else 0
        )
        return dataframe

    def create_adults_only_column(self, dataframe: pd.DataFrame):
        dataframe["adults_only"] = dataframe["rating"].isin(["R", "TV-MA"])
        return dataframe

    def run_transformations(self, dataframe: pd.DataFrame):

        dataframe.loc[dataframe["type"] == "Movie", "duration"] = dataframe.loc[
            dataframe["type"] == "Movie", "duration"
        ].apply(self.convert_movie_times_to_hours_and_minutes)

        dataframe = self.create_diversity_column(dataframe=dataframe)

        cleansed_dataframe = self.create_adults_only_column(dataframe=dataframe)

        return cleansed_dataframe

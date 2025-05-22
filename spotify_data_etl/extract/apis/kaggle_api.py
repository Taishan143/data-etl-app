import os
import base64
import requests
import logging
from dotenv import load_dotenv
import zipfile
import io
import pandas as pd

from spotify_data_etl.extract.extract_data import BaseAPIExtract
from spotify_data_etl.config.base_config import Config

from kaggle.api.kaggle_api_extended import KaggleApi


class KaggleAPI(BaseAPIExtract):

    def __init__(self, config: Config):
        super().__init__(config=config)
        self.api = KaggleApi()

    load_dotenv()
    USERNAME = os.getenv("BASIC_KAGGLE_USERNAME")
    KEY = os.getenv("BASIC_KAGGLE_KEY")

    def authenticate(self):
        """Authenticates to the Kaggle API."""

        os.environ["KAGGLE_USERNAME"] = self.USERNAME
        os.environ["KAGGLE_KEY"] = self.KEY
        self.api.authenticate()

    def extract_data(self):

        params = (
            f"?datasetVersionNumber={self.config.api.version}"
            if self.config.api.version
            else ""
        )

        url = (
            f"{self.config.base.base_url}/"
            + f"{self.config.base.endpoint}/"
            + f"{self.config.api.owner}/"
            + f"{self.config.api.dataset}"
            + params
        )
        credentials = base64.b64encode(
            bytes(f"{self.USERNAME}:{self.KEY}", "ISO-8859-1")
        ).decode("ascii")
        headers = {"Authorization": f"Basic {credentials}"}

        try:
            response = requests.get(url=url, headers=headers)
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            raise e

        zf = zipfile.ZipFile(io.BytesIO(response.content))

        filename = "netflix_titles.csv"
        dataframe = pd.read_csv(zf.open(filename))

        return dataframe

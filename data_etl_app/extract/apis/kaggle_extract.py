import os
import base64
import requests
import logging
from dotenv import load_dotenv
import zipfile
import io
import pandas as pd

from data_etl_app.extract.base_extractor import BaseAPIExtract
from data_etl_app.config.base_config import Config

from kaggle.api.kaggle_api_extended import KaggleApi


class KaggleExtract(BaseAPIExtract):

    def __init__(self, config: Config):
        super().__init__(config=config)
        self.api = KaggleApi()

        load_dotenv()
        self.USERNAME = os.getenv("BASIC_KAGGLE_USERNAME")
        self.KEY = os.getenv("BASIC_KAGGLE_KEY")

    def authenticate(self):
        """Authenticates to the Kaggle API."""

        os.environ["KAGGLE_USERNAME"] = self.USERNAME
        os.environ["KAGGLE_KEY"] = self.KEY
        self.api.authenticate()

    def extract_data(self) -> pd.DataFrame:

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
        dataframe = pd.read_csv(zf.open(filename), engine="python")

        return dataframe

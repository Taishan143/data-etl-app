from typing import Union, TypeAlias
from data_etl_app.extract.apis.kaggle_extract import KaggleExtract

Extractor: TypeAlias = Union[KaggleExtract]


def get_extractor_instance(api_name: str) -> Extractor:

    api_mapping: dict[str, Extractor] = {
        "kaggle": KaggleExtract,
    }
    try:
        return api_mapping[api_name]
    except KeyError:
        raise ValueError(f"No data extraction implementation found for: {api_name}")

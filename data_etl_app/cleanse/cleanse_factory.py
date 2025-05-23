from typing import Union, TypeAlias
from data_etl_app.cleanse.apis.kaggle_cleanser import KaggleDataCleanser

Cleanser: TypeAlias = Union[KaggleDataCleanser]


def get_cleanser_instance(api_name: str) -> Cleanser:

    api_mapping: dict[str, Cleanser] = {
        "kaggle": KaggleDataCleanser,
    }
    try:
        return api_mapping[api_name]
    except KeyError:
        raise ValueError(f"No data cleansing implementation found for: {api_name}")

from typing import Union, TypeAlias
from data_etl_app.visualisations.apis.kaggle_visualisations import KaggleVisualisations

Visualiser: TypeAlias = Union[KaggleVisualisations]


def get_visualisation_instance(api_name: str) -> Visualiser:

    api_mapping: dict[str, Visualiser] = {
        "kaggle": KaggleVisualisations,
    }
    try:
        return api_mapping[api_name]
    except KeyError:
        raise ValueError(f"No data visualisation implementation found for: {api_name}")

from typing import Union, TypeAlias
from data_etl_app.transform.apis.kaggle_transformer import KaggleTransformer

Transformer: TypeAlias = Union[KaggleTransformer]


def get_transformer_instance(api_name: str) -> Transformer:

    api_mapping: dict[str, Transformer] = {
        "kaggle": KaggleTransformer,
    }
    try:
        return api_mapping[api_name]
    except KeyError:
        raise ValueError(f"No data transformation implementation found for: {api_name}")

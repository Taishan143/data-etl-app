# flake8: noqa E501
from dataclasses import dataclass
import logging
from typing import Any, TypeAlias, Union

from spotify_data_etl.config.apis.kaggle import KaggleConfig, parse_kaggle_config

ApiConfig: TypeAlias = Union[KaggleConfig]


@dataclass
class BaseConfig:
    """A class for parsing config data."""

    api: str
    base_url: str
    endpoint: str

    def __post_init__(self):
        """Used for forcing types for each variable to ensure the correct data is parsed.

        :raises TypeError: Raised if any types do not match the dataclass inferred types.
        """
        fields_values_and_types = [
            (self.api, "api", str),
            (self.base_url, "base_url", str),
            (self.endpoint, "endpoint", str),
        ]

        for field_value, field, data_type in fields_values_and_types:
            if not isinstance(field_value, data_type):
                raise TypeError(
                    f"Expected {field}, with current value of {field_value}, to be {data_type.__name__}, got {type(field_value).__name__}."
                )


@dataclass
class Config:
    base: BaseConfig
    api: ApiConfig


def parse_base_config(config_data: Any):
    try:
        base = config_data["base"]
        return BaseConfig(
            api=base["api"],
            base_url=base["base_url"],
            endpoint=base["endpoint"],
        )
    except KeyError as kerr:
        raise KeyError(f"Missing required config key: {kerr}")


def parse_yaml_config(config_data: Any):
    base_config = parse_base_config(config_data=config_data)

    api = base_config.api

    match api:
        case "kaggle":
            api_config = parse_kaggle_config(config_data=config_data)
        case _:
            raise ValueError(f"Unsupported API type: {api}")

    return Config(base=base_config, api=api_config)

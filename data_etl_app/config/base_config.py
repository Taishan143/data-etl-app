# flake8: noqa E501
from dataclasses import dataclass
from typing import Any, TypeAlias, Union, Dict, Tuple, List, get_args, get_origin
from data_etl_app.config.apis.kaggle import KaggleConfig, parse_kaggle_config

ApiConfig: TypeAlias = Union[KaggleConfig]


@dataclass
class BaseConfig:
    """A class for parsing config data."""

    api: str
    base_url: str
    endpoint: str
    database_source: str

    def __post_init__(self):
        """Used for forcing types for each variable to ensure the correct data is parsed.

        :raises TypeError: Raised if any types do not match the dataclass inferred types.
        """
        fields_values_and_types = [
            (self.api, "api", str),
            (self.base_url, "base_url", str),
            (self.endpoint, "endpoint", str),
            (self.database_source, "database_source", str),
        ]

        for field_value, field, data_type in fields_values_and_types:
            if not isinstance(field_value, data_type):
                raise TypeError(
                    f"Expected {field}, with current value of {field_value}, to be {data_type.__name__}, got {type(field_value).__name__}."
                )


@dataclass
class DatabaseConfig:
    """A class for parsing database related information and queries."""

    name: str
    table: str
    queries: Dict[str, str]

    def __post_init__(self):
        """Used for forcing types for each variable to ensure the correct data is parsed.

        :raises TypeError: Raised if any types do not match the dataclass inferred types.
        """
        fields_values_and_types = [
            (self.name, "name", str),
            (self.table, "table", str),
            (self.queries, "queries", Dict[str, str]),
        ]

        validate_config_fields(variables_and_types=fields_values_and_types)


@dataclass
class Config:
    base: BaseConfig
    api: ApiConfig
    database: DatabaseConfig


def parse_base_config(config_data: Any):
    try:
        base = config_data["base"]
        return BaseConfig(
            api=base["api"],
            base_url=base["base_url"],
            endpoint=base["endpoint"],
            database_source=base["database_source"],
        )
    except KeyError as kerr:
        raise KeyError(f"Missing required base config key: {kerr}")


def parse_database_config(config_data: Any):
    try:
        database = config_data["database"]
        return DatabaseConfig(
            name=database["name"],
            table=database["table"],
            queries=database["queries"],
        )
    except KeyError as kerr:
        raise KeyError(f"Missing required database config key: {kerr}")


def parse_yaml_config(config_data: Any):
    base_config = parse_base_config(config_data=config_data)
    database_config = parse_database_config(config_data=config_data)

    api = base_config.api

    match api:
        case "kaggle":
            api_config = parse_kaggle_config(config_data=config_data)
        case _:
            raise ValueError(f"Unsupported API type: {api}")

    return Config(base=base_config, api=api_config, database=database_config)


def check_data_type(value, expected_type, field_name="unknown", errors=None):
    if errors is None:
        errors = []

    origin = get_origin(expected_type)
    args = get_args(expected_type)

    # Special case for typing.Any – skip check
    if expected_type is Any:
        return

    try:
        # Handle Dict[K, V]
        if origin is dict:
            if not isinstance(value, dict):
                raise TypeError(
                    f"{field_name}: Expected dict, got {type(value).__name__}"
                )
            key_type, val_type = args
            for k, v in value.items():
                check_data_type(k, key_type, f"{field_name}.key[{k}]", errors)
                check_data_type(v, val_type, f"{field_name}[{k}]", errors)
            return

        # Final base type check
        if not isinstance(value, expected_type):
            raise TypeError(
                f"{field_name}: Expected {expected_type.__name__}, got {type(value).__name__}"
            )

    except TypeError as err:
        errors.append(str(err))


def validate_config_fields(variables_and_types: List[Tuple]):
    errors = []
    for field_value, field_name, data_type in variables_and_types:
        check_data_type(
            value=field_value,
            expected_type=data_type,
            field_name=field_name,
            errors=errors,
        )
    if errors:
        raise TypeError("Type validation failed:\n" + "\n".join(errors))

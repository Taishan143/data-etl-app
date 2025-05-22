from dataclasses import dataclass
from typing import Any


@dataclass
class KaggleConfig:
    owner: str
    dataset: str
    version: int

    def __post_init__(self):
        """Used for forcing types for each variable to ensure the correct data is parsed.

        :raises TypeError: Raised if any types do not match the dataclass inferred types.
        """
        fields_values_and_types = [
            (self.owner, "owner", str),
            (self.dataset, "dataset", str),
            (self.version, "version", str),
        ]

        for field_value, field, data_type in fields_values_and_types:
            if not isinstance(field_value, data_type):
                raise TypeError(
                    f"Expected {field}, with current value of {field_value}, to be {data_type.__name__}, got {type(field_value).__name__}."
                )


def parse_kaggle_config(config_data: Any):
    try:
        api = config_data["api"]
        return KaggleConfig(
            owner=api["owner"],
            dataset=api["dataset"],
            version=api["version"],
        )
    except KeyError as kerr:
        raise KeyError(f"Missing required config key: {kerr}")

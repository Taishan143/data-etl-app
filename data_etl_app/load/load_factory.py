from typing import Union, TypeAlias
from data_etl_app.load.sources.mysql_loader import MySQLLoader
from data_etl_app.load.sources.sqlite_loader import SQLliteLoader

Loader: TypeAlias = Union[MySQLLoader]


def get_loader_instance(database_name: str) -> Loader:

    api_mapping: dict[str, Loader] = {"mysql": MySQLLoader, "sqlite": SQLliteLoader}
    try:
        return api_mapping[database_name]
    except KeyError:
        raise ValueError(f"No data loading implementation found for: {database_name}")

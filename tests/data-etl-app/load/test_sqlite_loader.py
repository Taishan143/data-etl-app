import unittest
import sqlite3

import pandas as pd
from unittest.mock import MagicMock, patch
from data_etl_app.load.sources.sqlite_loader import SQLliteLoader


class TestSQLiteLoader(unittest.TestCase):

    def setUp(self):
        mock_config = MagicMock()
        mock_config.database.name = "test_database.db"
        mock_config.database.table = "test_table"
        self.sqlite_loader = SQLliteLoader(config=mock_config)
        self.cursor = MagicMock()
        self.sqlite_loader.config.database.queries = {
            "create": "CREATE TABLE IF NOT EXISTS {table} (id INT PRIMARY KEY)"
        }

    @patch("data_etl_app.load.sources.sqlite_loader.sqlite3.connect")
    def test_create_connection__success(self, mock_sqlite_connect):
        # Arrange
        mock_sqlite_connect.return_value = "mock_connection"
        # Act
        result = self.sqlite_loader.create_connection()
        # Assert
        mock_sqlite_connect.assert_called_once_with(database="test_database.db")
        self.assertEqual(result, "mock_connection")

    @patch("data_etl_app.load.sources.sqlite_loader.sqlite3.connect")
    def test_create_connection__failure(self, mock_connect):
        # Arrange
        mock_connect.side_effect = sqlite3.OperationalError("Connection failed.")
        # Act
        with self.assertRaises(sqlite3.OperationalError) as context:
            self.sqlite_loader.create_connection()
        # Assert
        self.assertIn("Connection failed.", str(context.exception))

    def test_create_table__calls_with_correct_query(self):
        # Arrange
        expected_query = "CREATE TABLE IF NOT EXISTS test_table (id INT PRIMARY KEY)"
        # Act
        self.sqlite_loader.create_table(self.cursor)
        # Assert
        self.cursor.execute.assert_called_once_with(expected_query)

    @patch("data_etl_app.load.sources.sqlite_loader.pd.DataFrame.to_sql")
    def test_insert_data__calls_to_sql_correctly(self, mock_to_sql):
        # Arrange
        mock_df = pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]})
        mock_conn = MagicMock()
        # Act
        self.sqlite_loader.insert_data(connection=mock_conn, dataframe=mock_df)
        # Assert
        mock_to_sql.assert_called_once_with(
            "test_table", mock_conn, if_exists="replace", index=False
        )

    def test_show_data__executes_select_query(self):
        # Arrange
        expected_query = "SELECT * FROM test_table"
        # Act
        self.sqlite_loader.show_data(self.cursor)
        # Assert
        self.cursor.execute.assert_called_once_with(expected_query)

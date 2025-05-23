import unittest
import pandas as pd
from unittest.mock import MagicMock, patch
from data_etl_app.load.sources.mysql_loader import MySQLLoader


class TestMySQLLoader(unittest.TestCase):

    def setUp(self):

        mock_config = MagicMock()
        self.mysql_loader = MySQLLoader(config=mock_config)
        self.mysql_loader.config.database.name = "test_db"
        self.mysql_loader.host = "localhost"
        self.mysql_loader.user = "user"
        self.mysql_loader.password = "pass"
        self.mysql_loader.config.database.table = "test_table"
        self.mysql_loader.config.database.queries = {
            "create": "CREATE TABLE IF NOT EXISTS {table} (id INT PRIMARY KEY)"
        }

        self.cursor = MagicMock()

        self.data = [
            {
                "show_id": "s1",
                "title": "Test Show",
                "director": "Jane Doe",
                "rating": "PG",
            },
            {
                "show_id": "s2",
                "title": "Another Show",
                "director": "John Smith",
                "rating": "R",
            },
        ]

        self.dataframe = pd.DataFrame(self.data)

    @patch("data_etl_app.load.sources.mysql_loader.mysql.connector.connect")
    def test_create_connection_success(self, mock_connect):
        # Arrange
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        # Act
        conn = self.mysql_loader.create_connection()

        # Assert
        mock_connect.assert_called_once_with(
            host="localhost", user="user", password="pass", database="test_db"
        )
        self.assertEqual(conn, mock_conn)

    def test_create_table__calls_with_correct_query(self):
        # Arrange
        expected_query = "CREATE TABLE IF NOT EXISTS test_table (id INT PRIMARY KEY)"
        # Act
        self.mysql_loader.create_table(self.cursor)
        # Assert
        self.cursor.execute.assert_called_once_with(expected_query)

    def test_insert_data__calls_executemany_correctly(self):
        # Arrange
        test_dataframe = self.dataframe.copy()
        columns = list(test_dataframe.columns)
        placeholders = ", ".join(["%s"] * len(columns))
        update_cols = [col for col in columns if col != "show_id"]
        update_expr = ", ".join([f"{col}=VALUES({col})" for col in update_cols])
        expected_query = (
            f"INSERT INTO test_table ({', '.join(columns)}) VALUES ({placeholders})"
            f"ON DUPLICATE KEY UPDATE {update_expr}"
        )

        expected_data = [tuple(row) for row in test_dataframe.to_numpy()]

        # Act
        self.mysql_loader.insert_data(cursor=self.cursor, dataframe=test_dataframe)
        # Assert
        self.cursor.executemany.assert_called_once_with(expected_query, expected_data)

    def test_show_data__executes_select_query(self):
        # Arrange
        expected_query = "SELECT * FROM test_table"
        # Act
        self.mysql_loader.show_data(self.cursor)
        # Assert
        self.cursor.execute.assert_called_once_with(expected_query)

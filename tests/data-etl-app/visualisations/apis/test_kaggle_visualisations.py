import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
from data_etl_app.visualisations.apis.kaggle_visualisations import KaggleVisualisations


class TestKaggleVisualisations(unittest.TestCase):

    @patch("data_etl_app.visualisations.apis.kaggle_visualisations.pd.read_sql")
    def test_get_data(self, mock_read_sql):
        # Arrange
        sample_data = {"column1": [1, 2], "column2": ["A", "B"]}
        expected_df = pd.DataFrame(sample_data)
        mock_read_sql.return_value = expected_df

        mock_connection = MagicMock()

        kaggle_vis_client = KaggleVisualisations(config=MagicMock())

        # Act
        result_df = kaggle_vis_client.get_data(
            "SELECT * FROM your_table", mock_connection
        )

        # Assert
        mock_read_sql.assert_called_once_with(
            "SELECT * FROM your_table", mock_connection
        )
        mock_connection.close.assert_called_once()
        pd.testing.assert_frame_equal(result_df, expected_df)

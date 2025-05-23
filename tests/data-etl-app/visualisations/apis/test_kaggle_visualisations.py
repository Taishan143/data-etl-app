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

    def test_plot_data_calls_matplotlib_correctly(self):
        # Arrange
        df = pd.DataFrame(
            {"release_year": [2020, 2021, 2022], "diversity_score": [5, 7, 6]}
        )

        kaggle_vis_client = KaggleVisualisations(config=MagicMock())

        with patch("matplotlib.pyplot.scatter") as mock_scatter, patch(
            "matplotlib.pyplot.title"
        ), patch("matplotlib.pyplot.xlabel"), patch("matplotlib.pyplot.ylabel"), patch(
            "matplotlib.pyplot.grid"
        ), patch(
            "matplotlib.pyplot.tight_layout"
        ), patch(
            "matplotlib.pyplot.show"
        ):
            # Act
            kaggle_vis_client.plot_data(
                dataframe=df,
                columns=("release_year", "diversity_score"),
                title="Test Plot",
                xlabel="Year",
                ylabel="Score",
            )
            # Assert
            mock_scatter.assert_called_once_with(
                df["release_year"], df["diversity_score"]
            )

    def test_plot_data_raises_with_invalid_columns(self):
        # Arrange
        df = pd.DataFrame({"release_year": [2020], "diversity_score": [5]})
        kaggle_vis_client = KaggleVisualisations(config=MagicMock())

        # Act

        with self.assertRaises(ValueError) as context:
            kaggle_vis_client.plot_data(
                df, columns=("only_one_column",), title="", xlabel="", ylabel=""
            )

        # Assert
        self.assertIn(
            "Exactly two column names must be provided.", str(context.exception)
        )

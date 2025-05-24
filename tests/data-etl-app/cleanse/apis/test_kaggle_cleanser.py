import unittest
import pandas as pd
import numpy as np
from data_etl_app.cleanse.apis.kaggle_cleanser import KaggleDataCleanser


class TestKaggleCleanser(unittest.TestCase):

    def setUp(self):
        self.data = {
            "test_col_1": [1, 2, 3, np.nan],
            "test_col_2": ["a", "b", "c", np.nan],
            "date_added": [
                "September 12, 2024",
                "January 5, 2025",
                "March 14, 2025",
                np.nan,
            ],
            "director": ["Guy Ritchie", np.nan, "John Doe", "Alan Partridge"],
            "country": [np.nan, "England", "USA", "Brasil"],
            "cast": [
                "Chris Evans, Danny DeVito, Jonah Hill",
                "Simon Pegg, Nick Frost, Tom Cruise",
                np.nan,
                "John Barrowman, Kylie Minogue",
            ],
        }
        self.dataframe = pd.DataFrame(self.data)

    def test_reformat_date(self):
        # Arrange
        test_date = " September 12, 2024 "
        # Act
        kaggle_cleanser = KaggleDataCleanser()
        result = kaggle_cleanser.reformat_date(date_str=test_date)
        # Assert
        self.assertEqual(result, "2024-09-12")

    def test_reformat_date__null_date(self):
        # Arrange
        test_date = np.nan
        # Act
        kaggle_cleanser = KaggleDataCleanser()
        result = kaggle_cleanser.reformat_date(date_str=test_date)
        # Assert
        self.assertEqual(result, None)

    def test_reformat_date__unrecognised_value(self):
        # Arrange
        test_date = 12345
        # Act
        kaggle_cleanser = KaggleDataCleanser()
        result = kaggle_cleanser.reformat_date(date_str=test_date)
        # Assert
        self.assertEqual(result, None)

    def test_populate_null_values(self):
        # Arrange
        value = "d"
        column = "test_col_2"
        expected = pd.DataFrame(
            {
                "test_col_1": [1, 2, 3, np.nan],
                "test_col_2": ["a", "b", "c", "d"],
                "date_added": [
                    "September 12, 2024",
                    "January 5, 2025",
                    "March 14, 2025",
                    np.nan,
                ],
                "director": ["Guy Ritchie", np.nan, "John Doe", "Alan Partridge"],
                "country": [np.nan, "England", "USA", "Brasil"],
                "cast": [
                    "Chris Evans, Danny DeVito, Jonah Hill",
                    "Simon Pegg, Nick Frost, Tom Cruise",
                    np.nan,
                    "John Barrowman, Kylie Minogue",
                ],
            }
        )
        test_dataframe = self.dataframe.copy()
        # Act
        kaggle_cleanser = KaggleDataCleanser()
        kaggle_cleanser.populate_null_values(
            dataframe=test_dataframe, column=column, value=value
        )
        # Assert
        pd.testing.assert_frame_equal(test_dataframe, expected)

    def test_cleanse_data(self):
        # Arrange
        test_dataframe = self.dataframe.copy()
        expected = pd.DataFrame(
            {
                "test_col_1": [1, 2, 3, np.nan],
                "test_col_2": ["a", "b", "c", np.nan],
                "date_added": [
                    "2024-09-12",
                    "2025-01-05",
                    "2025-03-14",
                    None,
                ],
                "director": ["Guy Ritchie", "Unknown", "John Doe", "Alan Partridge"],
                "country": ["Unknown", "England", "USA", "Brasil"],
                "cast": [
                    "Chris Evans, Danny DeVito, Jonah Hill",
                    "Simon Pegg, Nick Frost, Tom Cruise",
                    "Unknown",
                    "John Barrowman, Kylie Minogue",
                ],
            }
        )
        # Act
        kaggle_cleaanser = KaggleDataCleanser()

        result = kaggle_cleaanser.cleanse_data(dataframe=test_dataframe)
        # Assert
        pd.testing.assert_frame_equal(result, expected)

import unittest
import pandas as pd
from data_etl_app.transform.apis.kaggle_transformer import KaggleTransformer


class TestKaggleTransformer(unittest.TestCase):

    def setUp(self):
        self.data = {
            "type": ["Movie", "TV", "Movie"],
            "duration": ["175 min", "3 seasons", "113 min"],
            "rating": ["R", "TV-MA", "PG-13"],
            "listed_in": [
                "Thriller,Action",
                "Documentaries",
                "Sci-fi,Thriller,Fantasy",
            ],
        }
        self.dataframe = pd.DataFrame(self.data)

    def test_convert_movie_times_to_hours_and_minutes(self):
        # Arrange
        test_time = "130min"
        expected = "2h 10m"
        # Act
        kaggle_transformer = KaggleTransformer()
        result = kaggle_transformer.convert_movie_times_to_hours_and_minutes(
            time_value=test_time
        )
        # Assert
        self.assertEqual(result, expected)

    def test_convert_movie_times_to_hours_and_minutes__None(self):
        # Arrange
        test_time = pd.NA
        expected = "Unknown"
        # Act
        kaggle_transformer = KaggleTransformer()
        result = kaggle_transformer.convert_movie_times_to_hours_and_minutes(
            time_value=test_time
        )
        # Assert
        self.assertEqual(result, expected)

    def test_create_diversity_column(self):
        # Arrange
        test_dataframe = self.dataframe.copy()
        expected = pd.DataFrame(
            {
                "type": ["Movie", "TV", "Movie"],
                "duration": ["175 min", "3 seasons", "113 min"],
                "rating": ["R", "TV-MA", "PG-13"],
                "listed_in": [
                    "Thriller,Action",
                    "Documentaries",
                    "Sci-fi,Thriller,Fantasy",
                ],
                "diversity_score": [2, 1, 3],
            }
        )
        # Act
        kaggle_transformer = KaggleTransformer()
        result = kaggle_transformer.create_diversity_column(dataframe=test_dataframe)
        # Assert
        print(result)
        pd.testing.assert_frame_equal(result, expected)

    def test_create_adults_only_column(self):
        # Arrange
        test_dataframe = self.dataframe.copy()
        expected = pd.DataFrame(
            {
                "type": ["Movie", "TV", "Movie"],
                "duration": ["175 min", "3 seasons", "113 min"],
                "rating": ["R", "TV-MA", "PG-13"],
                "listed_in": [
                    "Thriller,Action",
                    "Documentaries",
                    "Sci-fi,Thriller,Fantasy",
                ],
                "adults_only": ["Yes", "Yes", "No"],
            }
        )
        # Act
        kaggle_transformer = KaggleTransformer()
        result = kaggle_transformer.create_adults_only_column(dataframe=test_dataframe)
        # Assert
        pd.testing.assert_frame_equal(result, expected)

    def test_run_transformations(self):
        # Arrange
        test_dataframe = self.dataframe.copy()
        expected = pd.DataFrame(
            {
                "type": ["Movie", "TV", "Movie"],
                "duration": ["2h 55m", "3 seasons", "1h 53m"],
                "rating": ["R", "TV-MA", "PG-13"],
                "listed_in": [
                    "Thriller,Action",
                    "Documentaries",
                    "Sci-fi,Thriller,Fantasy",
                ],
                "diversity_score": [2, 1, 3],
                "adults_only": ["Yes", "Yes", "No"],
            }
        )
        # Act
        kaggle_transformer = KaggleTransformer()
        result = kaggle_transformer.run_transformations(dataframe=test_dataframe)
        # Assert
        pd.testing.assert_frame_equal(result, expected)

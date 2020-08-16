"""
This module tests most of the functions used throughout the package.
It is not possible to test the function process_netflix() and process_imdb()
found in data_processing.py, as these functions ingest and process all of the
data, which would take too much time. However, we do test all the functions
used inside process_netflix() and process_imdb().
"""
import os
import sys
import unittest
import pickle
import random
from pathlib import Path
import pandas as pd
import dash_html_components as html
import app.data.helper_functions as hf
import app.imdb_service as imdb
import app.netflix_service as nf
import app.web.choice_based_recommendation

sys.path.append('../data')


CSV_EXT = '.csv'
TAB = '\t'
NAS = ['\\N']
COMMA = ','

DATA_DIR = 'data'
TEST_DATA_DIR = 'test_files'
PROCESSED_DIR = 'pre_processed'
PATH_TO_TESTS = Path(__file__).parent
PATH_TO_DATA_TESTS = os.path.join(PATH_TO_TESTS.parent, DATA_DIR, TEST_DATA_DIR)
PATH_TO_DATA_PROC = os.path.join(PATH_TO_TESTS.parent, DATA_DIR, PROCESSED_DIR)


IMDB_TEST = 'imdb_df_test.csv'
IMDB_TITLES_TEST = 'imdb_titles_test.tsv'
IMDB_RATINGS_TEST = 'imdb_ratings_test.tsv'
IMDB_MERGED_COLS = ['tconst', 'titleType', 'primaryTitle', 'startYear',
                    'genres', 'averageRating', 'numVotes', 'weightedAverage']
GENRES_TEST = 'set_genres_test.pkl'
NF_RATINGS_TEST = 'netflix_test.txt'
NF_RATINGS_COLS = ['movie_id', 'user_id', 'rating', 'rating_date']
MOVIE_TITLES_RAW_TEST = 'movie_titles_raw_test.csv'
NF_MOVIE_TITLES_COLS = ['Sno', 'Year', 'Final_title', 'Display']
NF_DICT_RECOMMENDATIONS = 'dict_recommendations.pkl'

MOVIE_TITLES_TEST = 'movie_titles_test.csv'

CURRENT_DIR = '.'
TEST_FILE_OUT = 'test_file'

IMDB_URL = 'https://datasets.imdbws.com/title.ratings.tsv.gz'


class TestHelperFunctions(unittest.TestCase):
    """
    Test all the functions in helper_functions.py.
    """
    test_df = pd.DataFrame({'movies': ["A", "B", "C", "D"],
                            'genres': ["Action,Romance", "Comedy",
                                       "Comedy", "Romance"]})

    def test_unique_genres(self):
        """
        Check that the unique genres in the test_df have been correctly
        identified with the get_unique_genres(df) function.
        """
        self.assertEqual(
            hf.get_unique_genres(self.test_df),
            set(["Action", "Comedy", "Romance"]))

    def test_save_file(self):
        """
        Check that the save_file(file) function correctly outputs a csv file,
        then remove the created file.
        """
        hf.save_file(self.test_df, os.path.join(CURRENT_DIR), TEST_FILE_OUT, CSV_EXT)
        file_path = os.path.join(CURRENT_DIR, TEST_FILE_OUT+CSV_EXT)
        self.assertTrue(os.path.exists(file_path))
        os.system('rm '+file_path)

    def test_download_gz_file(self):
        """
        Checks that the function download_gz_file(url) generates a
        non-empty dataframe.
        """
        generated_df = hf.download_gz_file(IMDB_URL)
        self.assertGreater(len(generated_df), 0)

    def test_parse_data(self):
        """
        Checks that the function parse_data(file) parses the data from the file
        and outputs a list with the 10 ratings found in the test file.
        """
        file_path = os.path.join(PATH_TO_DATA_TESTS, NF_RATINGS_TEST)
        lst_data = hf.parse_data(file_path)
        self.assertEqual(len(lst_data), 10)

    def test_get_recommended_movies(self):
        """
        Checks that the function get_recommended_movies(df) outputs a dictionary with
        recommendations for the 3 movies in the test file.
        """
        file_path = os.path.join(PATH_TO_DATA_TESTS, NF_RATINGS_TEST)
        lst_data = hf.parse_data(file_path)
        df_netflix = pd.DataFrame(lst_data, columns=NF_RATINGS_COLS)
        self.assertEqual(len(hf.get_recommended_movies(df_netflix)), 3)

    def test_format_movie_titles(self):
        """
        Checks that the function format_movie_titles(file) processes the
        test file and adds the necessary columns. This function checks
        that the columns match with the desired output.
        """
        file_path = os.path.join(PATH_TO_DATA_TESTS, MOVIE_TITLES_RAW_TEST)
        movie_titles = hf.format_movie_titles(file_path)
        print(movie_titles)
        self.assertEqual(list(movie_titles.columns), NF_MOVIE_TITLES_COLS)

    def test_clean_imdb_data(self):
        """
        Checks that the function clean_imdb_data(df1, df2) processes and merges the
        test dataframes and adds calculates the necessary columns. This function checks
        that the columns match with the desired output.
        """
        titles_path = os.path.join(PATH_TO_DATA_TESTS, IMDB_TITLES_TEST)
        ratings_path = os.path.join(PATH_TO_DATA_TESTS, IMDB_RATINGS_TEST)
        titles_df = pd.read_csv(titles_path, sep=TAB, na_values=NAS)
        ratings_df = pd.read_csv(ratings_path, sep=TAB, na_values=NAS)
        merged_df = hf.clean_imdb_data(titles_df, ratings_df)
        self.assertEqual(list(merged_df.columns), IMDB_MERGED_COLS)

    def test_download_netflix_data(self):
        """
        The function download_netflix_data(user, directory) cannot be tested through
        Github because local Kaggle credentials are required,
        as described in our setup instructions.
        However, it can be tested locally using the following code:
        hf.download_netflix_data('netflix-inc', 'netflix-prize-data')
        self.assertTrue(os.path.exists('./netflix-prize-data'))
        os.system("rm -r netflix-prize-data")
        """
        pass


class TestImdb(unittest.TestCase):
    """
    Test all the function in imdb_service.py.
    """
    test_df = pd.DataFrame({
        'movies': ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"],
        'titleType': ["Movie", "Movie", "Movie", "tvSeries", "tvSeries",
                      "tvSeries", "tvSeries", "Movie", "tvSeries", "Movie",
                      "Movie"],
        'genres': ["Action", "Comedy", "Comedy", "Romance",
                   "Comedy,Romance", "Comedy,Action", "Romance",
                   "Action,Comedy", "Action", "Action", "Romance"],
        'startYear': [2020, 2019, 2018, 2020, 2016, 2015, 2012, 2017,
                      2016, 2019, 2018],
        'weightedAverage': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]})

    def test_load_data(self):
        """
        Checks that the function load_data(file) properly loads the desired file.
        """
        file_path = os.path.join(PATH_TO_DATA_TESTS, IMDB_TEST)
        original_file = pd.read_csv(file_path)
        self.assertEqual(len(imdb.load_data(file_path)), len(original_file))

    def test_load_genres(self):
        """
        Checks that the function load_genres(file) properly loads the list of genres.
        """
        file_path = os.path.join(PATH_TO_DATA_TESTS, GENRES_TEST)
        with open(file_path, 'rb') as file:
            original_file = pickle.load(file)
        self.assertEqual(imdb.load_genres(file_path), list(original_file))

    def test_filter_type(self):
        """
        Checks that the function filter_type(df, str) filters test_df
        correctly by 'titleType'.
        """
        self.assertEqual(len(imdb.filter_type(self.test_df, 'Movie')), 6)

    def test_filter_genre(self):
        """
        Checks that the function filter_genre(df, str) filters test_df
        correctly by 'genres'.
        """
        self.assertEqual(len(imdb.filter_genre(self.test_df, 'Action')), 5)

    def test_filter_year(self):
        """
        Checks that the function filter_year(df, int) filters test_df
        correctly by 'startYear'.
        """
        self.assertEqual(len(imdb.filter_year(self.test_df, 2018)), 2)

    def test_filter_top10(self):
        """
        Checks that the function filter_top10(df) gets the 10 rows with the
        highest 'weightedAverage' from test_df. As test_df only has 11 rows
        and the minimum 'weightedAverage' is 1, it checks that the minimum
        'weightedAverage' from the result is higher than 1.
        """
        self.assertGreater(imdb.filter_top10(self.test_df)['weightedAverage'].min(), 1)

    def test_filter_selected(self):
        """
        Checks that the function filter_selected(list, string) returns true when
        the string exists in the list.
        """
        self.assertTrue(imdb.filter_selected(["tvSeries", "Movie"], "Movie"))


class TestNetflix(unittest.TestCase):
    """
    Test all the function in netflix_service.py.
    """

    test_df = pd.DataFrame({
        'movies': ["M", "N", "P", "Q", "R", "S", "T", "U", "V", "X", "Y"],
        'titleType': ["Movie", "Movie", "Movie", "tvSeries", "tvSeries",
                      "Movie", "tvSeries", "Movie", "tvSeries", "Movie",
                      "tvSeries"],
        'genres': ["Action", "Comedy", "Romance", "Comedy",
                   "Comedy,Romance", "Comedy,Action", "Action",
                   "Action,Comedy", "Action", "Romance", "Romance"],
        'startYear': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017,
                      2018, 2019, 2020],
        'weightedAverage': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]})

    def test_reading_movie_title_csv(self):
        """
        Checks that the function reading_movie_title_csv(file) correctly loads
        the desired file.
        """
        file_path = os.path.join(PATH_TO_DATA_TESTS, MOVIE_TITLES_TEST)
        original_file = pd.read_csv(file_path)
        self.assertEqual(len(nf.reading_movie_title_csv(file_path)), len(original_file))

    def test_get_options(self):
        """
        Checks that the correct options list is generated in the get_options(lst) function.
        """
        file_path = os.path.join(PATH_TO_DATA_TESTS, MOVIE_TITLES_TEST)
        movies_df = pd.read_csv(file_path)
        dict_options = nf.get_options(movies_df['Display'].unique())
        self.assertEqual(len(movies_df), len(dict_options))

    def test_get_movie_id(self):
        """
        Checks that the correct Movie ID is retrieved from the dataframe.
        For the test, we used the movie 'Ricky Martin: One Night Only - 1999',
        with the corresponding ID 61.
        """
        file_path = os.path.join(PATH_TO_DATA_TESTS, MOVIE_TITLES_TEST)
        movies_df = pd.read_csv(file_path)
        title = 'Ricky Martin: One Night Only - 1999'
        movie_id = nf.get_movie_id(movies_df, title)
        self.assertEqual(movie_id, 61)

    def test_recommendation_for_movies(self):
        """
        Checks that the function recommendation_for_movies(file) loads a non-empty
        dictionary.
        """
        file_path = os.path.join(PATH_TO_DATA_PROC, NF_DICT_RECOMMENDATIONS)
        dict_recommendations = nf.recommendation_for_movies(file_path)
        self.assertTrue(len(dict_recommendations) > 0)

    def test_get_top10_movies(self):
        """
        CHecks that the function get_top10_movies(df, list1, list2) returns the info
        for the movie ids passed to the function.
        """
        file_path = os.path.join(PATH_TO_DATA_TESTS, MOVIE_TITLES_TEST)
        movies_df = nf.reading_movie_title_csv(file_path)
        movie_ids = list(range(1, 11))
        movie_scores = []
        for _ in movie_ids:
            movie_scores.append(random.uniform(0, 1))
        movies_info = nf.get_top10_movies(movies_df, movie_ids, movie_scores)
        self.assertEqual(len(movies_info), 10)

    def test_userchoice_based_movie_recommendation(self):
        """
        CHecks that the function userchoice_based_movie_recommendation(title, df, dictionary)
        returns the recommended movies for the selected title.
        """
        titles_path = os.path.join(PATH_TO_DATA_TESTS, MOVIE_TITLES_TEST)
        recs_path = os.path.join(PATH_TO_DATA_PROC, NF_DICT_RECOMMENDATIONS)
        movies_df = nf.reading_movie_title_csv(titles_path)
        dict_recommendations = nf.recommendation_for_movies(recs_path)
        title = 'Ricky Martin: One Night Only - 1999'
        movies_info = nf.userchoice_based_movie_recommendation(title, movies_df,
                                                               dict_recommendations)
        self.assertGreater(len(movies_info), 0)

    def test_generate_table(self):
        """
        Checks that the function generate_table(df, int) returns an html Table.
        """
        max_rows = 5
        table_output = app.web.choice_based_recommendation.generate_table(self.test_df, max_rows)
        self.assertTrue(isinstance(table_output, html.Table))


if __name__ == '__main__':
    unittest.main()

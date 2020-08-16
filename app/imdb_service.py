"""
This module defines the functions used in the tab2.py module.
"""
import pickle

import pandas as pd


def load_data(file_path):
    """
    Loading the imdb file located in file_path.
    Parameters:
        file_path = File path to the imdb pre_processed dataframe.
    Returns: The dataframe with the pre_processed imdb data.
    """
    imdb_df = pd.read_csv(file_path)
    return imdb_df


def load_genres(file_path):
    """
    Loading the genres located in file_path.
    Parameters:
        file_path = File path to the preprocessed genres set.
    Returns: A list with the unique genres.
    """
    with open(file_path, 'rb') as file:
        genres_set = pickle.load(file)
    return list(genres_set)


def filter_type(data, titletype: str):
    """
    Filters the data so that it only returns rows with the
    defined value 'titletype' in the field titleType.
    Parameters:
        data = IMDb dataframe that contains the column 'titleType'.
        titletype = String value used to filter the data.
    Returns: A dataframe with rows that have the value 'titletype'
    in the field titleType.
    """
    return data[data['titleType'].str.contains(titletype)]


def filter_genre(data, genre: str):
    """
    Filters the data so that it only returns rows that contain the
    defined 'genre' in their column genres.
    Parameters:
        data = IMDb dataframe that contains the column 'genres'.
        genre = String value used to filter the data.
    Returns: A dataframe with rows that contain the value 'genre'
    in the field genres.
    """
    return data[data['genres'].str.contains(genre)]


def filter_year(data, year_selected: int):
    """
    Filters the data so that it only returns rows that contain the
    defined 'year_selected' in their column startYear.
    Parameters:
        data = IMDb dataframe that contains the column 'startYear'.
        year_selected = String value used to filter the data.
    Returns: A dataframe with rows that have the value 'year_selected'
    in the field startYear.
    """
    return data[data['startYear'].astype(int) == year_selected]


def filter_top10(data):
    """
    Gets the top ten rows based on the weightedAverage column.
    Parameters:
        data = IMDb dataframe that contains the column 'weightedAverage'.
    Returns: A dataframe with the ten rows with the largest
    'weightedAverage' value.
    """
    return data.nlargest(10, 'weightedAverage')


def filter_selected(list_values, value):
    """
    Check if a value exists in a list.
    Parameters:
        list_values = A non-empty list.
        value = A value
    Returns: True if the value exists in the list.
    """
    return value in list_values

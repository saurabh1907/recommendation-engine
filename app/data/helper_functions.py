"""
This module defines all the functions used in the data_processing.py
module.
"""
import pickle
import urllib.request
import gzip
import os
import zipfile

import pandas as pd
import numpy as np
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity


ZIP_EXT = '.zip'
CSV_EXT = '.csv'
ENC = 'iso8859_2'
NF_TITLES_COLS = ['Sno', 'Year', 'Final_title', 'Display']
TAB = '\t'
NAS = ['\\N']
TYPE_FILTER = ['movie', 'tvSeries']
COL_SUBSET = ['tconst', 'titleType', 'primaryTitle', 'startYear', 'genres']

def download_netflix_data(user, directory):
    """
    Download Netflix dataset from Kaggle and unzip directory.
    Parameters:
        user = Kaggle user owner of the dataset.
        directory = directory name that is downloaded.
    Returns: Directory unzipped in the current working directory.
    """
    nf_file = directory+ZIP_EXT
    #os.system('kaggle datasets download -d netflix-inc/netflix-prize-data')
    os.system('kaggle datasets download -d '+user+'/'+directory)
    with zipfile.ZipFile(nf_file, 'r') as zip_ref:
        zip_ref.extractall(directory)
    os.remove(nf_file)
    print('The', directory, 'dataset was downloaded and unzipped.')


def parse_data(file_path):
    """
    Parse the movie ratings file into something usable.
    Parameters:
        file_path = path to the file to be parsed.
    Retuns: List with data in a usable format.
    """
    file_open = open(file_path, 'rt')
    file_data = file_open.readlines()
    final_list = []
    for line in file_data:
        if ':' in line:
            current_movie_id = int(line[:-2])
        elif ',' in line:
            tmp = line[:-1].split(',')
            item = [current_movie_id, int(tmp[0]), int(tmp[1]), tmp[2]]
            final_list.append(item)
    print('Done parsing file: ', file_path)
    return final_list


def get_recommended_movies(movies):
    """
    Creating a dictionary with the recommended movies, based on the
    cosine similarity between them.
    Parameters:
        movies = Dataframe with all the movie ratings per user.
    Returns: Dictionary with the recommended movies for each movie id.
    """
    sparse_data = sparse.csr_matrix((movies.rating,
                                     (movies.user_id, movies.movie_id)))
    similarity = cosine_similarity(sparse_data.T, dense_output=False)
    movie_ids = np.unique(similarity.nonzero())
    similar_movies_dict = dict()
    for movie in movie_ids:
        rec_movies_ids = np.argsort(-similarity[movie].toarray().ravel())[1:100]
        score_lst = sorted(similarity[movie].toarray().ravel(), reverse=True)
        rec_movies_score = np.array(score_lst[1:100])
        similar_movies_dict[movie] = [rec_movies_ids, rec_movies_score]
    print('Done creating cosine similarity dictionary')
    return similar_movies_dict


def format_movie_titles(titles_path):
    """
    Remove the commas in the movie title and adds the Display column.
    Parameters:
        titles_path = path to the movie_titles file from the Netflix data.
    Returns: A dataframe with the formatted data.
    """
    with open(titles_path, 'r', encoding=ENC) as file:
        data = file.readlines()
    final_list = []
    for line in data:
        current_line = line[:-1]
        current_line.replace('NULL', '')
        tmp = current_line.split(',', 2)
        title = tmp[2].replace(",", "")
        new_item = [int(tmp[0]), tmp[1], title, title+' - '+tmp[1]]
        final_list.append(new_item)
    movie_titles = pd.DataFrame(final_list, columns=NF_TITLES_COLS)
    return movie_titles


def download_gz_file(url):
    """
    Download and unzip tsv file.
    Parameters:
        url = URL where the file is stored.
    Returns: Downloaded file in a dataframe.
    """
    file_name = url.split("/")[-1]
    testfile = urllib.request.URLopener()
    testfile.retrieve(url, file_name)
    with gzip.open(file_name) as file_open:
        df_data = pd.read_csv(file_open, sep=TAB, na_values=NAS)
    os.remove(file_name)
    return df_data


def clean_imdb_data(df_titles, df_ratings):
    """
    Cleaning the IMDb data: keeping only tv series and movies, merging
    the dataframes to get the ratings for each observation, and
    calculating the weighted average.
    Parameters:
        df_titles = Dataframe with all the titles from IMDb.
        df_ratings = Dataframe with the ratings for all the titles
                    from IMDb.
    Returns: Cleaned and merged dataframe.
    """
    types_filter = df_titles.titleType.isin(TYPE_FILTER)
    df_titles = df_titles[types_filter][COL_SUBSET]
    df_merged = df_titles.merge(df_ratings, how='left', left_on='tconst',
                                right_on='tconst')
    df_merged['titleType'] = df_merged['titleType'].astype(str)
    df_merged = df_merged.dropna()
    df_merged['weightedAverage'] = df_merged['averageRating']*df_merged['numVotes']
    print('Done cleaning and merging IMDb data')
    return df_merged


def get_unique_genres(df_movies):
    """
    Obtains a unique list of possible genres.
    Parameters:
        df_movies = Complete IMDb dataframe.
    Returns: A set with the unique genres.
    """
    genres_all = list(df_movies['genres'].unique())
    genres_list = [element for item in genres_all for element in item.split(',')]
    genres_unique = set(genres_list)
    return genres_unique


def save_file(obj, directory, file_name, ext):
    """
    Saves the object in the specified directory. The method used depends
    on the extension.
    Parameters:
        obj = Python object to store.
        directory = Folder where to store the object.
        file_name = File name to use when storing the object.
        ext = Extension of the file to store.
    Returns: The saved file in the desired location.
    """
    if ext == CSV_EXT:
        obj.to_csv(os.path.join(directory, file_name+ext), index=False)
    else:
        with open(os.path.join(directory, file_name+ext), 'wb') as file_open:
            pickle.dump(obj, file_open, protocol=pickle.HIGHEST_PROTOCOL)
    print('Done storing file: ', file_name+ext)

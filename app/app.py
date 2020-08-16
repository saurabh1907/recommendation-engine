"""
This is the main file that hosts the web-app. It has dash app initialization and callouts.
"""
import os
import dash
from dash.dependencies import Input, Output

from app import netflix_service as nmr
from app import imdb_service
from app.web import layout

# Loading the necessary files: movies_df, imdf_df, dict_rec
DATA_FOLDER = 'data'
BINGEWATCH_FOLDER = 'app'
PRE_PROCESSED_DIR = 'pre_processed'
DATASET_DIR = 'dataset'
MOVIES_FILE = 'movie_titles.csv'
IMDB_FILE = 'imdb_df.csv'
GENRE_FILE = 'set_genres.pkl'
DICT_REC = 'dict_recommendations.pkl'

DATA_DIR = os.path.join(BINGEWATCH_FOLDER, DATA_FOLDER)
MOVIES_FILE_PATH = os.path.join(DATA_DIR, DATASET_DIR, MOVIES_FILE)
IMDB_PATH = os.path.join(DATA_DIR, DATASET_DIR, IMDB_FILE)
GENRES_PATH = os.path.join(DATA_DIR, PRE_PROCESSED_DIR, GENRE_FILE)
DICT_REC_PATH = os.path.join(DATA_DIR, PRE_PROCESSED_DIR, DICT_REC)

IMDB_DF = imdb_service.load_data(IMDB_PATH)
MOVIES_DF = nmr.reading_movie_title_csv(MOVIES_FILE_PATH)
GENRES = imdb_service.load_genres(GENRES_PATH)
DICT_REC = nmr.recommendation_for_movies(DICT_REC_PATH)

EXTERNAL_STYLESHEETS = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS)
app.config.suppress_callback_exceptions = True

app.layout = layout()

## Late Import to avoid circular import
from app.web import choice_based_recommendation, filter_based_recommendation


@app.callback(Output('tabs-content-display', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    """
    This function displays tabs based on user selection of tab
    """
    if tab == 'tab-2':
        return filter_based_recommendation.TAB2_LAYOUT
    return choice_based_recommendation.CHOICE_BASED_RECOMMENDATION_LAYOUT


## Tab-1: Choice Based Recommendation
@app.callback(Output('my-table', 'children'), [Input('movie_list_input', 'value')])
def update_table(selected_movie):
    """
    It returns the html table of top 10 movies
    Args:
        selected_movie: user input of movie title
    Returns: Html table of 10 movies
    """
    movie_list = nmr.userchoice_based_movie_recommendation(selected_movie, MOVIES_DF, DICT_REC)
    return choice_based_recommendation.generate_table(movie_list)


@app.callback(Output('my-scatter-plot', 'figure'), [Input('movie_list_input', 'value')])
def update_figure(selected_movie):
    """
    This returns bar plot of movies along match scores
    Args:
        selected_movie: user input of movie title
    Returns: Bar plot of movies & match %age
    """
    movie_list2 = nmr.userchoice_based_movie_recommendation(selected_movie, MOVIES_DF, DICT_REC)
    return choice_based_recommendation.update_figure(movie_list2)

## Tab2:Genre/Time Based_recommendation callback
@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('filter-checklist', 'value'),
     Input('year-slider', 'value'),
     Input('title-type', 'value'),
     Input('genre-dropdown', 'value')
     ])
def update_figure_tab2(selected_filters, selected_year, selected_type, selected_genre):
    """
    Returns bar plot of movies with their weighted average
    """
    genre_filtered = imdb_service.filter_selected(selected_filters, 'Genre')
    year_filtered = imdb_service.filter_selected(selected_filters, 'Year')

    final_df = imdb_service.filter_type(IMDB_DF, selected_type)
    if genre_filtered and selected_genre:
        final_df = imdb_service.filter_genre(final_df, selected_genre)
    if year_filtered and selected_year:
        final_df = imdb_service.filter_year(final_df, selected_year)

    final_df = imdb_service.filter_top10(final_df)

    return filter_based_recommendation.update_figure(final_df)

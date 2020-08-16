"""
This module contains the layout for the second tab of the visualization.
It is being called by main.py.
"""
import dash_html_components as html
import dash_core_components as dcc
from app.app import IMDB_DF
from app.app import GENRES


EXTERNAL_STYLESHEETS = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
YEAR_MIN = max(int(IMDB_DF['startYear'].min()), 1950)
YEAR_MAX = int(IMDB_DF['startYear'].max())


TAB2_LAYOUT = html.Div([
    html.Div([
        html.Label('Filter by:'),
        dcc.Checklist(
            id='filter-checklist',
            options=[
                {'label': 'Genre', 'value': 'Genre'},
                {'label': 'Year', 'value': 'Year'}],
            value=['Genre', 'Year'])],
             style={'margin-bottom': '50px', 'margin-left':'20px'}),
    html.Div(id='slider-wrapper', children=[
        html.Label('Year: (Please select the desired year)'),
        dcc.Slider(
            id='year-slider',
            min=YEAR_MIN,
            max=YEAR_MAX,
            value=int(IMDB_DF['startYear'].max()),
            marks={
                1950: {'label': '1950', 'style': {'color': '#77b0b1'}},
                1960: {'label': '1960', 'style': {'color': '#77b0b1'}},
                1970: {'label': '1970', 'style': {'color': '#77b0b1'}},
                1980: {'label': '1980', 'style': {'color': '#77b0b1'}},
                1990: {'label': '1990', 'style': {'color': '#77b0b1'}},
                2000: {'label': '2000', 'style': {'color': '#77b0b1'}},
                2010: {'label': '2010', 'style': {'color': '#77b0b1'}},
                2015: {'label': '2015', 'style': {'color': '#77b0b1'}},
                2020: {'label': '2020', 'style': {'color': '#77b0b1'}}
            },
            included=False,
            updatemode='drag',
            tooltip={'always_visible': True})],
             style={'margin-bottom': '50px',
                    'margin-left': '20px',
                    'margin-right': '20px',
                    'text-orientation': 'mixed'}),
    html.Div([
        html.Div([
            html.Label('Select the genre you would like to see:'),
            dcc.Dropdown(
                id='genre-dropdown',
                options=[{'label': i, 'value': i} for i in GENRES],
                placeholder='Select Genre',)],
                 style={'width': '48%',
                        'margin-bottom': '50px',
                        'margin-left':'20px',
                        'display': 'inline-block'}),
        html.Div([
            html.Label('Select the type of content you would like to see:'),
            dcc.RadioItems(
                id='title-type',
                options=[{'label': 'Movie', 'value' : 'movie'},
                         {'label' :'TV Series', 'value': 'tvSeries'}],
                value='movie',
                labelStyle={'display': 'inline-block', 'padding': '10px'})],
                 style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
        ]),

    html.Div([
        dcc.Graph(style={'height': '400px',
                         'width': '1300px',
                         'margin-left':'auto',
                         'margin-right':'auto'},
                  id='graph-with-slider')])
    ])


def update_figure(data):
    return {
        'data': [{'x': data['primaryTitle'], 'y': data['weightedAverage'], 'type': 'bar'}],
        'layout': dict(
            hovermode='closest',
            # height = 500,
            title='Top 10 Most Popular',
            yaxis={'title': 'Weighted Average'})
    }
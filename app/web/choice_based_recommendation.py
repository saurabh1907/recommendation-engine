""" This is dash layout file for Personal Choice based Recommendation.
    It is being called in app.py
"""
import dash_html_components as html
import dash_core_components as dcc
from app.app import MOVIES_DF
from app import netflix_service as nmr

COLORS = {
    'background': 'white',
    'background1': 'light blue',
    'text': 'black'
}

CHOICE_BASED_RECOMMENDATION_LAYOUT = html.Div(
    style={'backgroundColor': COLORS['background']}, children=[
        html.Div(className='div-user-controls',
                 children=[
                     html.H4(children='Enter a movie you have loved watching: ',
                             style={
                                 'textAlign': 'left',
                                 'color': COLORS['text']
                             }),
                     html.Div(
                         className='div-for-dropdown-and-table',
                         children=[
                             dcc.Dropdown(id='movie_list_input',
                                          options=nmr.get_options(MOVIES_DF['Display'].unique()),
                                          value=[MOVIES_DF['Display'].iloc[61]],
                                          searchable=True,
                                          placeholder="Select a movie"
                                          ),
                         ],
                         style={'width': '50%', 'text': 'black', 'font': 'Times New Roman',
                                'background': COLORS['background1']}
                     ),
                     html.Div(children=[html.H1("\n \n")]),
                     html.Div(id='after_input_text',
                              children=[html.P("\n\nWe believe based on your liking "
                                               "for the above movie, the following "
                                               "10 movies will interest you the most:")],
                              style={'text-orientation': 'left'}
                              )
                 ]
                 ),
        html.Div(id='output',
                 className='row',
                 children=[html.Div(id='my-table',
                                    className='five columns'),
                           html.Div(dcc.Graph(id='my-scatter-plot'),
                                    className='seven columns')
                           ]
                 )
    ]
)


def generate_table(dataframe, max_rows=10):
    """
    It generates a html table which is used in choice_based_recommendation.py file
    to show the top 10 recommended movies to users based on selected choice
    Args:
        dataframe: Pandas dataframe containing the details of recommended movies
        max_rows: Maximum rows to be displayed in the html table
    Returns:  Html table with 10 movies
    """
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

def update_figure(movie_list):
    return {
        'data': [{'x': movie_list['Movie Title'], 'y': movie_list['Match%'], 'type': 'bar'}],
        'layout': dict(
            hovermode='closest',
            title='Top 10 Most Recommended',
            yaxis={'title': 'Match%'},
            margin={'l': 45, 'b': 150, 't': 40, 'r': 15}
        )
    }
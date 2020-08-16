import dash_html_components as html
import dash_core_components as dcc

COLORS = {
    'background': 'white',
    'background1': 'light blue',
    'text': 'black'
}

def layout():
    return html.Div(style={'backgroundColor': COLORS['background']},
                      children=[
                          html.H1(
                              children='Movie Recommendation: Get your next watch here!',
                              style={
                                  'textAlign': 'center',
                                  'color': COLORS['text']
                              }
                          ),
                          html.Div(
                              children='Get your next watch just by entering '
                                       'either your favorite movie or your preferred genre '
                                       'or any time period. Tell us your choice & we will find'
                                       'the relevant movies and/or tv series '
                                       'that will absolutely delight you! So, lets go!!\n \n',
                              style={
                                  'textAlign': 'center',
                                  'color': COLORS['text']
                              }
                          ),
                          html.Div(children=''
                                            ''
                                            ''
                                            ''
                                   ),
                          dcc.Tabs(id="tabs-example", value='tab-1',
                                   children=[
                                       dcc.Tab(label='Choice Based Recommendation',
                                               value='tab-1'),
                                       dcc.Tab(label='Filter Based Recommendation',
                                               value='tab-2'),
                                   ]),
                          html.Div(id='tabs-content-display')
                      ])
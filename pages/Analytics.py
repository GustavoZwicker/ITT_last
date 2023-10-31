from dash import Dash, html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import json

import dash

colors = {
    'background': '#F0EBEA',
    'white': '#F4F6F7',
    'itt': '#17BDF7',
    'gray': '#A4A9AA',
    'light-gray': '#C9C9C9',
    'blue-light': '#67D2F7',
    'yellow': '#DFD536',
    'red': '#E8270D',
    'black': '#000000',
    'dark-gray': '#5A5A5A'
}

dash.register_page(__name__, path='/')

# Página "analytics"
layout = html.Div([
    dcc.Store('input_value', storage_type='memory'),
    html.Div([dcc.Link(dbc.Button('< Back', size="lg", outline=True, className="back",
                        style={
                            "margin-top": "20px",
                            'width': '10%',
                            'color': colors['itt']
                        }), href="/home", refresh=True)], style={'display': 'inline-block'}),
    html.Div([
    html.H1(
        children='ITT- Is That True?',
        style={'textAlign': 'center',
               'margin': '30px',
               'color': colors['itt']}),
    html.Div(
        [
            dcc.Textarea(
                id='input',
                placeholder='Insert here the text you want to Analyze',
                style={
                        'width': '50%',
                        'height': '100px',
                        'lineHeight': '25px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '40px',
                        'color': colors['dark-gray'],
                        'padding': 15
                    },
            ),
            html.H1(
                children='Text Language: ',
                style={'textAlign': 'center',
                       'font-size': '16px',
                       'color': colors['dark-gray']}),
            dcc.Dropdown(id='choose_language',
                options={
                        'pt': 'Portuguese-BR',
                        'en':'English'
                },
                value='Montreal',
                # style={
                #         'width': '200px',
                #         'height': '20px',
                #         'textAlign': 'justify',
                #         'color': colors['dark-gray']
                #     }
                style={'margin':'auto', 'width':'200px', 'textAlign': 'justify'}
                ),
            html.Br(),
            html.P(id='output')
        ],
        style={'textAlign': 'center'}
    ),
    # dbc.Row([html.H2(
    #     children='-------------------- OR --------------------',
    #     style={
    #         'textAlign': 'center',
    #         'color': colors['gray'],
    #         'fontSize': '15px'
    #     }
    # )
    # ], justify='center'),

    dbc.Button('Analyze', size="lg", id="analyze_button", n_clicks=0,
               outline=True, className="analyze", color="primary",
               style={
                   "margin-top": "10px",
                   'width': '32%',
                   'display': 'inline-block'},
               ), html.Div(children=html.Div(id='redirect'))
        ], style={'textAlign': 'center'})
        ]
)

# Callbacks para a página "analytics"


@callback(
    Output('input_text', 'data'),
    [
        Input('analyze_button', 'n_clicks'),
        Input('input', 'value')
    ]
)
def get_input(analyze_button, input_model):
    if analyze_button != 0:
        print(input_model)
        return input_model

@callback(
    Output('language', 'data'),
    [
        Input('analyze_button', 'n_clicks'),
        Input('choose_language', 'value')
    ]
)
def get_input(analyze_button, choose_language):
    if analyze_button != 0:
        print(choose_language)
        return choose_language
    
@callback(
    Output('redirect', 'children'),
    Input('analyze_button', 'n_clicks')
)
def redirect(analyze_button):
    if analyze_button != 0:
        return [dcc.Location(id='to_result', href='/results')]

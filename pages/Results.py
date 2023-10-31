from dash import Dash, html, dcc, callback, Input, Output, State, callback, dash_table
import numpy as np
import pandas as pd
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
import dash_bootstrap_components as dbc
import dash
from ITT_model import ITT  # Importe a classe ITT do módulo main
import base64


if 'itt_instance' not in globals():
    itt_instance = ITT()

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

test_png = r'Assets/Images/Raster.png'
test_base64 = base64.b64encode(open(test_png, 'rb').read()).decode('ascii')

dash.register_page(__name__, path='/results')

layout = html.Div([
    dcc.Link(dbc.Button('< Back', size="lg", outline=True, className="back",
                        style={
                            "margin-top": "20px",
                            "margin-bottom": "20px",
                            'width': '10%',
                            'color': colors['itt'],
                            'background-color': 'white !important',
                            'marginLeft': '5%'
                        }
                        ), href="/", refresh=True),
    html.Div(html.B('Results'), style= {'fontSize': 80, 'fontWeight': 'bold', 'textAlign': 'center', "margin-bottom": "80px"}),

    html.Div([
    html.Div(id='itt-output', style={'margin-bottom':'200px'}),
    html.Div([
        html.Span(html.B('Suggested articles for further reading'),
                  style={
                      'fontSize': 40,
                      'textAlign': 'center',
                      'margin-top': '20px',
                      'color': colors['gray'],
                      'display': 'block',
                      'margin-bottom': '40px'}),
    html.Div([
    dash_table.DataTable(
        columns=[
            {"name": 'Title', "id": 'title', "selectable": True},
            {"name": 'Source', "id": 'site', "selectable": True}
        ],
        style_table={'maxWidth': '600px', 'margin': '0 auto'},  
        style_header={
            'backgroundColor': colors['itt'],
            'fontWeight': 'bold',
            'color': 'white',
            'textAlign': 'center',
            'fontSize': '20px'
        },
        data=pd.DataFrame(data=[['Lorem ipsum', 'Lorem ipsum'] for i in range(10)], columns=['title', 'site']).to_dict('records'),
        style_cell={'textAlign': 'center',
                    'padding': '10px',
                    'color': 'black',
                    'fontWeight': 'bold',
                    'fontSize': '15px'},
        css=[{"selector": ".show-hide", "rule": "display: none"}]
    )
], style={'text-align': 'center', 'margin-bottom': '80px', 'marginLeft': '5%', 'marginRight': '5%'})
    ],
    )
]),

html.Div([
    html.A(
        dbc.Button(children= [
            html.Div([
                html.Img(src='data:image/png;base64,{}'.format(test_base64), style={'height': '30px', 'margin-top': '10px'
}),
                html.Div("About our Model", style= {'font-size': '16px', 'color': 'gray', 'margin-top': '10px'})
            ], style={'display': 'flex','flex-direction': 'column', 'align-items': 'center'}),
        ], className='buttom-class',  color= colors['background']
), href= "/about"
    )
], style= {'marginLeft': '5%'})



], style={'marginLeft': 'auto', 'marginRight': 'auto'}


)

# @callback(
#     Output('output_text', 'data'),
#     Input('output_text', 'data'))
# def pass_input_to_destination(input_model):
#     return input_model

@callback(
    Output('itt-output', 'children'),
    [
        Input('input_text', 'data'),
        Input('language', 'data')
    ]
    )
def get_result(input_model, language):
    # itt_instance = ITT(glove_model)  # Instancie a classe ITT
    # itt_instance.text = input_model  # Defina o texto a ser analisado
    print(f'RESULT: {input_model}')
    
    output_text = itt_instance.Analyse(input_model, language)

    return html.Div([
        html.Span('The inputted text has a', style={'color': colors['dark-gray'], 'fontSize': 30, 'font-style': 'italic'}),
        html.Span(' ', style={'white-space': 'pre'}),  # Espaço antes do output_text
        html.Span(html.B(output_text), style={'color': colors['red'], 'fontSize': 50}),
        html.Span(' ', style={'white-space': 'pre'}),  # Espaço após o sinal de %
        html.Span(html.B('%'), style={'color': colors['red'], 'fontSize': 50}),
        html.Span(' ', style={'white-space': 'pre'}),  # Espaço após o %
        html.Span('chance of being a Fake News', style={'color': colors['dark-gray'], 'fontSize': 30, 'font-style': 'italic'})
    ], style={'text-align': 'center', 'marginLeft': '5%','marginRight': '5%'})






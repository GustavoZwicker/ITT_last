import dash
import dash_bootstrap_components as dbc
import json
from dash import Dash, html, dcc, callback, Input, Output, State
from gensim.models import KeyedVectors

colors = {
    'background': '#F0EBEA',
    'white': '#F4F6F7',
    'itt': '#17BDF7',
    'gray': '#A4A9AA',
    'light-gray': '#C9C9C9',
    'blue-light': '#67D2F7'
}

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout= html.Div([dcc.Store('input_text', data=[] ,storage_type='session'), dcc.Store('language', data=[] ,storage_type='session')  
                    ,dash.page_container])
# app.layout= html.Div([dcc.Store('result_text', storage_type='session'), dash.page_container])

# app.run_server(debug=True, host="0.0.0.0")
app.run_server(debug=True)

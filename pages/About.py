import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output
from googletrans import Translator
import base64
import dash_bootstrap_components as dbc

test_png = r'Assets\Images\home.png'
test_base64 = base64.b64encode(open(test_png, 'rb').read()).decode('ascii')

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



dash.register_page(__name__, path='/about')


layout = html.Div([


    html.Div([
        html.A(
            dbc.Button(children= [
                html.Div([
                    html.Img(src='data:image/png;base64,{}'.format(test_base64), style={'height': '30px', 'margin-top': '10px'
    }),
                    html.Div("Home", style= {'font-size': '20px', 'color': colors['itt'], 'margin-top': '10px'})
                ], style={'display': 'flex','flex-direction': 'column', 'align-items': 'center'}),
            ], className='buttom-class',  color= colors['background']
    ), href= "/home"
        )
    ], style={'margin-top': '20px', 'marginLeft': '5%', 'marginRight': '5%'}),

    html.H1(id="about-header", style= {'textAlign': 'center', 'margin-top': '100px'}),
    dcc.Dropdown(
        id='language-dropdown',
        options=[
            {'label': 'Português', 'value': 'pt'},
            {'label': 'English', 'value': 'en'},
        ],
        value='pt',
        style= {'width': '150px', 'marginLeft': '5%', 'marginRight': '5%'}
    ),
    html.Div(id='about-text', style= {'fontSize': 20, 'margin-top': '30px', 'marginLeft': '5%', 'marginRight': '5%', 'textAlign': 'justify', 'margin-bottom': '50px'})
])

@callback(
    [Output('about-header', 'children'), Output('about-text', 'children')],
    Input('language-dropdown', 'value')
)

def update_about_text(selected_language):

    if selected_language == 'pt':
        about_header = html.Span("Sobre Nós", style={'color': colors['itt'], 'fontSize': 50, 'fontWeight': 'bold'})
        about_text = [
            html.Span("ITT- Is That True?", style={'color': colors['itt'], 'fontSize': 30, 'fontWeight': 'bold'}),
            " É um aplicativo da Web com o objetivo de tornar a verificação de fatos mais fácil. Fazemos isso usando técnicas de Machine Learning para Processamento de Linguagem Natural e, eventualmente, nosso modelo é capaz de identificar as características de uma ",
            html.Span("Fake News", style={'color': 'red', 'fontSize': 30, 'fontWeight': 'bold'}),
            ". Para isso, treinamos nosso modelo usando dados disponíveis na web. Atualmente, estamos em uma versão de testes, treinada com o conjunto de dados conhecido como ",
            html.Span("FakeBr. Corpus", style={'color': colors['itt'], 'fontSize': 30, 'fontWeight': 'bold'}),
            ", que contém",
            html.Span("7.200", style={'color': colors['itt'], 'fontSize': 30, 'fontWeight': 'bold'}),
            " amostras de textos falsos e verdadeiros. É importante enfatizar que esta versão ainda não está pronta para ser divulgada ao público e que os dados usados para treinamento ainda não representam com precisão a realidade."
        ]
    
    elif selected_language == 'en':
        about_header = html.Span("About Us", style={'color': colors['itt'], 'fontSize': 50, 'fontWeight': 'bold'})
        about_text = [
             html.Span("ITT- Is That True?", style={'color': colors['itt'], 'fontSize': 30, 'fontWeight': 'bold'}),
            " Is an Web Application that aims to make fact checking easier to the public. For that, we are using Machine Learning and Natural Language Processing techniques, so that our model can eventually learn to distinguish ",
            html.Span("Fake News", style={'color': 'red', 'fontSize': 30, 'fontWeight': 'bold'}),
            " characteristics. To do that, we have trained our model using data available on the web. Currently, we are on a test version, trained using the ",
            html.Span("LIAR", style={'color': colors['itt'], 'fontSize': 30, 'fontWeight': 'bold'}),
            " dataset, containing",
            html.Span("12.800", style={'color': colors['itt'], 'fontSize': 30, 'fontWeight': 'bold'}),
            " text samples. We consider it extremely important to emphasize that this version is not yet ready for public disclosure and use, and the data used for training do not yet accurately represent reality."
        ]

    return about_header, about_text

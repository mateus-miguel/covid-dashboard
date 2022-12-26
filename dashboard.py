import dash
# import dash_core_components as dcc
# import dash_html_components as html
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import plotly.express as px
import plotly.graph_objects as go

import numpy as np
import pandas as pd
import json

# O .csv tem dados Brasil, Estados, Municípios e aqui é filtrado os dados do Brasil e Estados em dois .csv separados
# df = pd.read_csv('HIST_PAINEL_COVIDBR_13mai2021.csv', sep=';')
# df_states = df[(~df['estado'].isna()) & (df['codmun'].isna())] # Separa somente os dados de estados, sem Brasil ou de municípios
# df_brasil = df[df['regiao'] == 'Brasil'] # Apenas dados do Brasil todo
# df_brasil.to_csv('df_brasil.csv')
# df_states.to_csv('df_states.csv')

df_states = pd.read_csv('df_states.csv')
df_brasil = pd.read_csv('df_brasil.csv')
a = df_states[(df_states['estado'] == 'RO') & (df_states['data'] == '2021-05-13')]
a['casosAcumulado'].values[0]


df_states_ = df_states[df_states['data'] == '2020-05-13']
brazil_states = json.load(open('geojson/brazil_geo.json', 'r'))
df_data = df_states[df_states['estado'] == 'RJ']
# brazil_states
# type(brazil_states)
# brazil_states.keys()
# brazil_states["features"][0].keys()
# brazil_states['features'][0]['id']
# df_states.columns # casosAcumulado, casosNovos, obitosAcumulado, obitosNovos
select_columns = {
    'casosAcumulado': 'Casos Acumulados',
    'casosNovos': 'Casos por dia',
    'obitosAcumulado': 'Óbitos Totais',
    'obitosNovos': 'Óbitos por dia'
}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG]) # módulo dash instanciando classe Dash

fig = px.choropleth_mapbox(df_states_, locations='estado', color='casosNovos', 
                            geojson=brazil_states, center={'lat': -16.95, 'lon': -47.78}, zoom=4, 
                            color_continuous_scale='Redor', opacity=0.4, 
                            hover_data={'casosAcumulado': True, 'casosNovos': True, 'obitosNovos': True, 'estado': True}) 
fig.update_layout(
    paper_bgcolor='#242424',
    autosize=True,
    margin=go.Margin(l=0, r=0, t=0, b=0),
    showlegend=False,
    mapbox_style = 'carto-darkmatter'
)                           
# mapbox é uma API externa que cria gráficos bonitos
# locations tem a coluna 'estado' do df_states para associar à chave 'id' do geojson
# color pintará com base nos dados de 'casosNovos' em cada estado
# hover_data contém as colunas que serão exibidas, do df_states, ao passar o mouse por cada estado

fig2 = go.Figure(layout={'template': 'plotly_dark'})
fig2.add_trace(go.Scatter(x=df_data['data'], y=df_data['casosAcumulado']))
fig2.update_layout(
    paper_bgcolor='#242424',
    plot_bgcolor='#242424',
    autosize=True,
    margin=dict(l=10, r=10, t=10, b=10)
)

# URL = Uniform Resource Locator, endereço de rede onde se encontra certo recurso como um arquivo
# Contâiner das linhas e colunas do app Dash, uma com o mapa do geojson e outra com dados do df_states
app.layout = dbc.Container(
    dbc.Row([
        dbc.Col([
            html.Div([
                #html.Img(id='logo', src=app.get_asset_url('logo_dark.png'), height=50),
                html.H6('Evolução COVID-19'),
                dbc.Button('BRASIL', color='primary', id='location-button', size='lg')
            ], style={}),
            html.P('Informe a data na qual deseja obter informações:', style={'margin-top': '20px'}),
            html.Div(id='div-test', children=[
                dcc.DatePickerSingle(
                    id='date-picker',
                    min_date_allowed=df_brasil['data'].min(),
                    max_date_allowed=df_brasil['data'].max(),
                    initial_visible_month=df_brasil['data'].min(),
                    date=df_brasil['data'].max(),
                    display_format='MMMM D, YYYY',
                    style={'border': '0px solid black'}
                )
            ]),

            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span('Casos recuperados', style={'font-size': '13px'}),
                            html.H3(style={'color': '#adfc92'}, id='casos-recuperados-text'),
                            html.Span('Em acompanhamento', style={'font-size': '13px'}),
                            html.H5(id='em-acompanhamento-text')
                        ])
                    ], color='light', outline=True, style={'margin-top': '10px', 'box-shadow': '0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)', 'color': '#FFFFFF'})
                ], md=4),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span('Casos confirmados', style={'font-size': '13px'}),
                            html.H3(style={'color': '#389fd6'}, id='casos-confirmados-text'),
                            html.Span('Novos casos na data', style={'font-size': '13px'}),
                            html.H5(id='novos-casos-text')
                        ])
                    ], color='light', outline=True, style={'margin-top': '10px', 'box-shadow': '0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)', 'color': '#FFFFFF'})
                ], md=4),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span('Óbitos confirmados', style={'font-size': '13px'}),
                            html.H3(style={'color': '#df2935'}, id='obitos-text'),
                            html.Span('Óbitos na data', style={'font-size': '13px'}),
                            html.H5(id='obitos-na-data-text')
                        ])
                    ], color='light', outline=True, style={'margin-top': '10px', 'box-shadow': '0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)', 'color': '#FFFFFF'})
                ], md=4)
            ]),
            
            html.Div([
                html.P('Selecione que tipo de dado deseja visualizar:', style={'margin-top': '25px'}),
                dcc.Dropdown(id='location-dropdown',
                            options=[{'label': j, 'value': i} for i, j in select_columns.items()],
                            value='casosNovos',
                            style={'margin-top': '10px'}),
                dcc.Graph(id='line-graph', figure=fig2)
            ])
        ], md=5, style={'padding': '25px', 'background-color': '#242424'}),

        dbc.Col([
            dcc.Loading(id='loading-1', type='default', 
                        children=[
                            dcc.Graph(id='cloropeth-map', figure=fig, style={'height': '100vh', 'margin-right': '10px'})
                        ])
        ], md=7)
    ], className='g-0')
, fluid=True, style={'width': '100%', 'height': '100%'})

# -------------------------------------------------------
# Interactivity

@app.callback(
    [
        Output('casos-recuperados-text', 'children'),
        Output('em-acompanhamento-text', 'children'),
        Output('casos-confirmados-text', 'children'),
        Output('novos-casos-text', 'children'),
        Output('obitos-text', 'children'),
        Output('obitos-na-data-text', 'children')
    ], 
    [Input('date-picker', 'date'), Input('location-button', 'children')]
)
def display_status(date, location):
    if location == 'Brasil':
        df_data_on_date = df_brasil[df_brasil['data'] == date]
    else:
        df_data_on_date = df_states[(df_states['estado'] == location) & (df_states['data'] == date)]

    recuperados_novos = '-' if df_data_on_date['Recuperadosnovos'].isna().values[0] else df_data_on_date['Recuperadosnovos'].values[0]
    acompanhamentos_novos = '-' if df_data_on_date['emAcompanhamentoNovos'].isna().values[0] else df_data_on_date['emAcompanhamentoNovos'].values[0]
    casos_acumulados = '-' if df_data_on_date['casosAcumulado'].isna().values[0] else df_data_on_date['casosAcumulado'].values[0]
    casos_novos = '-' if df_data_on_date['casosNovos'].isna().values[0] else df_data_on_date['casosNovos'].values[0]
    obitos_acumulado = '-' if df_data_on_date['obitosAcumulado'].isna().values[0] else df_data_on_date['obitosAcumulado'].values[0]
    obitos_novos = '-' if df_data_on_date['obitosNovos'].isna().values[0] else df_data_on_date['obitosNovos'].values[0]
    return (recuperados_novos,
            acompanhamentos_novos,
            casos_acumulados,
            casos_novos,
            obitos_acumulado,
            obitos_novos)

if __name__ == '__main__':
    app.run_server(debug=True)
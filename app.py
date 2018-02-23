# -*- coding: utf-8 -*-
import dash_dangerously_set_inner_html
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import os

import pandas as pd
from pandas_datareader import data as web
import geopandas as gpd

app = dash.Dash(__name__)
server = app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

colors = {
    'background': '#FFFFFF',
    'text': '#333333',
    'H1': '#222222',
    'H2': '#b489d1',
    'H3': '#4DA3F6'
}

gdf = gpd.read_file('data/pov_emissionsFresno.shp')

markdown_text = '.'

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='CEC 2020',
        style={
            'textAlign': 'left',
            'color': colors['H1']
        }
    ),

    # html.Div(children='', style={
    #     'textAlign': 'left',
    #     'color': colors['text']
    # }),

    html.H3(children='Poverty Percentile to PM2.5 Emissions Scatter Plot', style={
        'textAlign': 'left',
        'color': colors['H3']
    }),

    dcc.Dropdown(
        id='pov-emissions-dropdown',
        options=[
            {'label': 'Fresno', 'value': 'Fresno'},
            {'label': 'Los Angeles', 'value': 'LA'}
        ],
        value='Fresno'
    ),
    dcc.Graph(
        id='pov-emissions',
        figure={
            'data': [
                go.Scatter(
                    x=gdf[gdf['Tract_1'] == i]['Pov_pctl'],
                    y=gdf[gdf['Tract_1'] == i]['PM2.5T'],
                    # text=gdf[gdf['Tract_1'] == i]['Tract_1'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in gdf.Tract_1.unique()
            ],
            'layout': go.Layout(
                xaxis={'type': 'log', 'title': 'Poverty Percentile (Statewide)'},
                yaxis={'title': 'PM2.5 (Raw)'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest',
                # title='\nFresno Poverty Percentile to PM2.5 Emissions Scatter Plot'
            )
        }
    ),

    # dcc.Graph(
    #     id='pov-emissions-map',
    #     figure={
    #         'data': [
    #             go.Choropleth(
    #                 locationmode = "ISO-3",
    #                 locations = gdf[gdf['Tract_1'] == i]['Tract_1'],
    #                 z = gdf[gdf['Tract_1'] == i]['PM2.5T'],
    #                 text = gdf[gdf['Tract_1'] == i]['Tract_1'],
    #                 colorscale = [[0,'rgb(0, 0, 0)'],[1,'rgb(0, 0, 0)']],
    #                 autocolorscale = False,
    #                 showscale = False,
    #                 # geo = 'geo2'
    #                 geo = gdf[gdf['Tract_1'] == i]['geometry'].to_json()
    #             ) for i in gdf.Tract_1.unique()
    #         ]
    #         # 'layout': go.Layout(
    #         #     xaxis={'type': 'log', 'title': 'Poverty Percentile (Statewide)'},
    #         #     yaxis={'title': 'PM2.5 (Raw)'},
    #         #     margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
    #         #     legend={'x': 0, 'y': 1},
    #         #     hovermode='closest',
    #         #     title=''
    #         # )
    #     }
    # ),

    html.H3(children='Example', style={
        'textAlign': 'left',
        'color': colors['H3']
    }),

    dcc.Graph(
        id='example-graph-2',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    ),

    html.Div([
        dash_dangerously_set_inner_html.DangerouslySetInnerHTML('''
            <style>.embed-container {position: relative; padding-bottom: 80%; height: 0; max-width: 100%;} .embed-container iframe, .embed-container object, .embed-container iframe{position: absolute; top: 0; left: 0; width: 100%; height: 100%;} small{position: absolute; z-index: 40; bottom: 0; margin-bottom: -15px;}</style><div class="embed-container"><iframe width="500" height="400" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" title="pop health" src="//www.arcgis.com/apps/Embed/index.html?webmap=f66e9be609df4049967e36c1de32f128&amp;extent=-123.1827,35.4058,-116.0966,37.8868&zoom=true&previewImage=false&scale=true&legend=true&disable_scroll=true&theme=light"></iframe></div>
        '''),
    ]),

    dcc.Markdown(children=markdown_text)
])

@app.callback(Output('pov-emissions', 'figure'), [Input('pov-emissions-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    gdf = gpd.read_file('data/pov_emissions' + selected_dropdown_value + '.shp')

        # web.DataReader(
        # selected_dropdown_value, data_source='google',
        # start=dt(2017, 1, 1), end=dt.now()
        # )
    return {
        'data': [
            go.Scatter(
                x=gdf[gdf['Tract_1'] == i]['Pov_pctl'],
                y=gdf[gdf['Tract_1'] == i]['PM2.5T'],
                # text=gdf[gdf['Tract_1'] == i]['Tract_1'],
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 15,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name=i
            ) for i in gdf.Tract_1.unique()
        # {
        #     'x': gdf[gdf['Tract_1'] == i]['Pov_pctl'],
        #     'y': gdf[gdf['Tract_1'] == i]['PM2.5T']
        # }
        ],
        'layout': go.Layout(
            xaxis={'type': 'log', 'title': 'Poverty Percentile (Statewide)'},
            yaxis={'title': 'PM2.5 (Raw)'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest',
            # title='\nFresno Poverty Percentile to PM2.5 Emissions Scatter Plot'
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)

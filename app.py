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

app.css.append_css({"external_url": "https://fonts.googleapis.com/css?family=Prata"})
app.css.append_css({"external_url": "https://cdn.rawgit.com/CSFlorin/RAPELIC_Web/master/style.css"})
# app.css.append_css({"external_url": "https://rawgit.com/CSFlorin/RAPELIC_Web/master/style.css"})
# dcc._css_dist[0]['relative_package_path'].append('style.css')


colors = {
    'background': '#FFFFFF',
    'text': '#333333',
    'gray': '#3E3E3E',
    'black': '#2E2E2E',
    'H3': '#4DA3F6'
}

gdf = gpd.read_file('data/pov_emissionsFresno.shp')
gdf2 = gpd.read_file('data/pov_emissionsFresno_0.shp')

markdown_text = '.'

app.layout = html.Div(className="everything", style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Reduction of Pollutant Health Damages in California',
        style={
            'textAlign': 'center',
            'color': colors['gray']
        }
    ),
    html.P(
        children='By FLORIN LANGER | Reporting from Berkeley, Calif.',
        style={
            'textAlign': 'center',
            'color': colors['gray']
        }
    ),
    html.Div(
        className="article",
        children=[
            html.Div(
                className="row",
                children=[
                    html.Div(
                        className="six columns",
                        children=[
                            html.Div(
                                children=[
                                html.H4(children='Poverty Percentile to PM2.5 Emissions Scatter Plot over Blockgroups', style={
                                    'textAlign': 'left',
                                    'color': colors['black']
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
                                )
                                ]
                            )
                        ]
                    ),

                    html.Div(
                        className="six columns",
                        children=html.Div([
                            html.H4(children='Poverty to Asthma Percentile PM2.5 Scatter Plot over Blockgroups', style={
                                'textAlign': 'left',
                                'color': colors['black']
                            }),
                            dcc.Dropdown(
                                id='pov-emissions-dropdown2',
                                options=[
                                    {'label': 'Fresno', 'value': 'Fresno'},
                                    {'label': 'Los Angeles', 'value': 'LA'}
                                ],
                                value='Fresno'
                            ),
                            dcc.Graph(
                                id='pov-emissions2',
                                figure={
                                    'data': [
                                        go.Scatter(
                                            x=gdf2[gdf2['Tract_1'] == i]['Pov_pctl'],
                                            y=gdf2[gdf2['Tract_1'] == i]['Asthma_Pct'],
                                            # text=gdf[gdf['Tract_1'] == i]['Tract_1'],
                                            mode='markers',
                                            opacity=0.7,
                                            marker={
                                                'size': gdf2[gdf2['Tract_1'] == i]['PM2.5T'],
                                                'line': {'width': 0.5, 'color': 'white'}
                                            },
                                            name=i
                                        ) for i in gdf2.Tract_1.unique()
                                    ],
                                    'layout': go.Layout(
                                        xaxis={'type': 'log', 'title': 'Poverty Percentile (Statewide)'},
                                        yaxis={'title': 'Asthma Percentile (Statewide)'},
                                        margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                                        legend={'x': 0, 'y': 1},
                                        hovermode='closest',
                                        # title='\nFresno Poverty Percentile to PM2.5 Emissions Scatter Plot'
                                    )
                                }
                            )

                        ])
                    )
                ]
            )
        ]
    ),

    html.Div(
        className="row",
        children=[
            html.Div(
                className="six columns",
                children=[
                    html.Div(
                        children=[
                        html.H4(children='Poverty Percentile over Census Tracts', style={
                            'textAlign': 'left',
                            'color': colors['black']
                        }),
                        html.Div(style={
                            'textAlign': 'left',
                            'color': colors['text'],
                            # 'width': '40%',
                            'height': '400'
                            },
                            children=[
                                html.Iframe(style={'border': 'none', 'width': '100%', 'height': '100%'},srcDoc='<style>.embed-container {position: relative; padding-bottom: 67%; height: 0; max-width: 100%;} .embed-container iframe, .embed-container object, .embed-container iframe{position: absolute; top: 0; left: 0; width: 100%; height: 100%;} small{position: absolute; z-index: 40; bottom: 0; margin-bottom: -15px;}</style><div class="embed-container"><iframe width="600" height="400" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" title="pop health" src="//www.arcgis.com/apps/Embed/index.html?webmap=f66e9be609df4049967e36c1de32f128&amp;extent=-123.1827,35.4058,-116.0966,37.8868&zoom=true&previewImage=false&scale=true&legend=true&disable_scroll=true&theme=light"></iframe></div>'),
                            ]
                        )
                        ]
                    )
                ]
            ),

            html.Div(
                className="six columns",
                children=html.Div([
                    html.P(children='A description\nof\nthe\nmap\non\nthe\nleft', style={
                        'textAlign': 'left',
                        'color': colors['gray']
                    })

                ])
            )
        ]
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

    html.H4(children='Example', style={
        'textAlign': 'left',
        'color': colors['black']
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


    # html.Div([
    #     dash_dangerously_set_inner_html.DangerouslySetInnerHTML('''
    #         <style>.embed-container {position: relative; padding-bottom: 80%; height: 0; max-width: 100%;} .embed-container iframe, .embed-container object, .embed-container iframe{position: absolute; top: 0; left: 0; width: 100%; height: 100%;} small{position: absolute; z-index: 40; bottom: 0; margin-bottom: -15px;}</style><div class="embed-container"><iframe width="500" height="400" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" title="pop health" src="//www.arcgis.com/apps/Embed/index.html?webmap=f66e9be609df4049967e36c1de32f128&amp;extent=-123.1827,35.4058,-116.0966,37.8868&zoom=true&previewImage=false&scale=true&legend=true&disable_scroll=true&theme=light"></iframe></div>
    #     '''),
    # ]),

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


@app.callback(Output('pov-emissions2', 'figure'), [Input('pov-emissions-dropdown2', 'value')])
def update_graph(selected_dropdown_value):
    gdf2 = gpd.read_file('data/pov_emissions' + selected_dropdown_value + '_0.shp')

        # web.DataReader(
        # selected_dropdown_value, data_source='google',
        # start=dt(2017, 1, 1), end=dt.now()
        # )
    return {
        'data': [
            go.Scatter(
                x=gdf2[gdf2['Tract_1'] == i]['Pov_pctl'],
                y=gdf2[gdf2['Tract_1'] == i]['Asthma_Pct'],
                # text=gdf[gdf['Tract_1'] == i]['Tract_1'],
                mode='markers',
                opacity=0.7,
                marker={
                    'size': gdf2[gdf2['Tract_1'] == i]['PM2.5T'],
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name=i
            ) for i in gdf2.Tract_1.unique()
        ],
        'layout': go.Layout(
            xaxis={'type': 'log', 'title': 'Poverty Percentile (Statewide)'},
            yaxis={'title': 'Asthma Percentile (Statewide)'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest',
            # title='\nFresno Poverty Percentile to PM2.5 Emissions Scatter Plot'
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)

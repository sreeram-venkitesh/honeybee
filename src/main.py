import dash
from dash.dependencies import Input,Output,State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from steem import Steem
from pick import pick
import pprint
import json


app = dash.Dash()

app.title = 'honeybee'
app.layout = html.Div(
    children=[
    html.Div(
        className='app-header',
        children=[
            html.H1('honeybee'),
            html.H2('The Hive Data Collector'),
        ]
    ),
    html.Div(
        style={'text-align':'center','align-items':'center'},
        children=[
           dcc.Input(id='tag',value="",className='text-area'),
            dcc.Input(id='posts',value="",className='text-area'),
            html.Button('Get Data!',id='button',className='button-css')
        ]
    ),
    html.Div(
        children=[
            html.H1(id='output'),
        ]
    ),
    dbc.Tooltip("Enter your tags here",target="tag"),
    dbc.Tooltip('Enter the number of posts here',target='posts')
    
    ],)


@app.callback(
    Output(component_id='output',component_property='children'),
    [Input(component_id='button',component_property='n_clicks')],
    state=[State(component_id='tag',component_property='value'),State(component_id='posts',component_property='value')]
    )
def update(clicks,tag,post):
    return 'You have clicked {} times. Input tags are {}, number of posts are {}'.format(clicks,tag,post)
    
    

if __name__ == "__main__":
    app.run_server(debug=True,port='8020')


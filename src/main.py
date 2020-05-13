import dash
import dash_core_components as dcc
import dash_html_components as html

from steem import Steem
from pick import pick
import pprint
import json

app = dash.Dash()

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
            html.Textarea(id='tag',title='tags',placeholder="Enter Tags",rows=1,className='text-area'),
            html.Textarea(id='posts',title='No. of posts',placeholder="Enter number of posts",rows=1,className='text-area'),
            html.Button('Get Data!',id='button',className='button-css')
        ]
    ),
    html.Div(
        children=[
            html.H1('Some content goes here'),
        ]
    )
    
    ],)

if __name__ == "__main__":
    app.run_server(debug=True)


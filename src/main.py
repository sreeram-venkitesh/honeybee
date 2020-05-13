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
           dcc.Input(id='tag',value="",className='text-area',placeholder='Enter Tags'),
            dcc.Input(id='posts',value="",className='text-area',placeholder='Enter Number of Posts'),
            html.Button('Get Data!',id='button',className='button-css')
        ]
    ),
    html.Div(
        children=[
            html.H3(id='output'),
        ]
    ),    
    ],)


@app.callback(
    Output(component_id='output',component_property='children'),
    [Input(component_id='button',component_property='n_clicks')],
    state=[State(component_id='tag',component_property='value'),State(component_id='posts',component_property='value')]
    )
def update(clicks,tag,post):
    s = Steem()
    query = {
        "limit":post, #number of posts
        "tag":str(tag) #tag of posts
        }
    print("working on it ")
    posts = s.get_discussions_by_created(query)
    options = []
    #posts list options
    # string = ""
    details=""
    print("working")
    for post in posts:
        options.append(post["author"]+'/'+post["permlink"])
        details += str(s.get_content(post["author"],post["permlink"]))
        details += '\n\n\n'

    # return 'You have clicked {} times. Input tags are {}, number of posts are {}'.format(clicks,tag,post)
    return details
    

    

if __name__ == "__main__":
    app.run_server(debug=True,port='8020')


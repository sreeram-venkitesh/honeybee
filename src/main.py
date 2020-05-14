import dash
from dash.dependencies import Input,Output,State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_dangerously_set_inner_html as dds

import os
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
        style={'text-align':'center'},
        children=[
        dcc.Dropdown(id='option-select',
            className='option-select',
            placeholder='Select Operation',
            options=[
                {'label':'Get Latest Post','value':'latest'},
                {'label':'Get Post Analytics','value':'analytics'},
                {'label':'Get Post Metadata','value':'metadata'}]),
                html.Br(),
                dcc.Input(id='tag',value="",className='text-area',placeholder='Enter Tags',disabled=True),
                dcc.Input(id='posts',value="",className='text-area',placeholder='Enter Number of Posts',type='number',disabled=True),
                html.Button('Get Data!',id='button',className='button-css')
        ]
    ),
    html.Div(
        style={'text-align':'center'},
        children=[  
            html.Iframe(id='output',className='output-class'),
            #dds.DangerouslySetInnerHTML(component_id='output')
        ]
    ),    
    ],)

@app.callback(
    [Output(component_id='tag',component_property='disabled'),
    Output(component_id='posts',component_property='disabled')],
    [Input(component_id='option-select',component_property='value')]
)
def option_select(val):
    if(val=='latest'):
        return False,True
    elif val=='analytics':
        return False,False
    elif val=='metadata':
        return False,False
    else:
        return True,True

@app.callback(
    Output(component_id='output',component_property='srcDoc'),
    [Input(component_id='button',component_property='n_clicks')],
    state=[State(component_id='option-select',component_property='value'),State(component_id='tag',component_property='value'),State(component_id='posts',component_property='value')]
    )
def update(clicks,option,tag,post):

    if(option=='latest'):
        post=1

        s = Steem()
        query = {
            "limit":post, #number of posts
            "tag":str(tag) #tag of posts
            }
        print("collecting posts...")
        posts = s.get_discussions_by_created(query)
        print('posts collected!')

        details = ''
        dicts = []
        print("working")
        for post in posts:
            details = s.get_content(post["author"],post["permlink"])
            dicts.append(details)
            
        print(type(details))
        # # return 'You have clicked {} times. Input tags are {}, number of posts are {}'.format(clicks,tag,post)
        post_info = "Post Info <br><br>Author : {} <br><br>Category : {} <br><br>Created : {} <br><br>Title : {} <br><br>Body : {}".format(dicts[0]['author'],
         dicts[0]['category'],dicts[0]['created'],dicts[0]['title'],dicts[0]['body'])
        #print(post_info)
        # return str(dicts[0].keys())
        return post_info  
    
    elif(option=='analytics'):
        s = Steem()
        query = {
            "limit":post, #number of posts
            "tag":str(tag) #tag of posts
            }
        print("collecting posts...")
        posts = s.get_discussions_by_created(query)
        print('posts collected!')

        details = ''
        dicts = []
        print("working")
        for post in posts:
            details = s.get_content(post["author"],post["permlink"])
            dicts.append(details)

        pending = []
        for post in dicts:
            pending.append(post['pending_payout_value'])
        print(type(pending[0]))
        numbers = []
        for entry in pending:
            for word in entry.split():
                print(word)
                try:
                    numbers.append(float(word))
                except:
                    print()
        
        return str(numbers)
        

    
    


if __name__ == "__main__":
    app.run_server(debug=True,port='8040')


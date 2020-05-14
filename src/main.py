import dash
from dash.dependencies import Input,Output,State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import os
from steem import Steem
from pick import pick
import pprint
import json



# def steemfunc(post,tag):
#     s = Steem()
#     query = {
#         "limit":post, #number of posts
#         "tag":str(tag) #tag of posts
#         }
#     print("collecting posts...")
#     posts = s.get_discussions_by_created(query)
#     print('posts collected!')
#     options = []
#     #posts list options
#     details = ''
#     dicts = []
#     print("working")
#     for post in posts:
#         options.append(post["author"]+'/'+post["permlink"])
#         details = s.get_content(post["author"],post["permlink"])

#         # string += json.dumps(details,indent=4)
#         # string += '\n\n'
#         dicts.append(details)
#         # text_file = open('steem_posts.txt','wt')
#         # n = text_file.write(str(string))
#         # text_file.close()

#         # data = json.load(open('steem_posts.txt'))
#         # pending_payouts.append(data['pending_payout_value'])
#         # os.remove('steem_posts.txt')
    
        

#     # print(pending_payouts)
#     print(type(details))
#     # print(dicts[2]['pending_payout_value'])
#     # print('pending payout :')
#     # print(data[0]['pending_payout_value'])
#     # return 'You have clicked {} times. Input tags are {}, number of posts are {}'.format(clicks,tag,post)
#     return dicts


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
        children=[
            html.P(id='output',className='output-class'),
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
    Output(component_id='output',component_property='children'),
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
    options = []
    #posts list options
    details = ''
    dicts = []
    print("working")
    for post in posts:
        options.append(post["author"]+'/'+post["permlink"])
        details = s.get_content(post["author"],post["permlink"])

        # string += json.dumps(details,indent=4)
        # string += '\n\n'
        dicts.append(details)
        # text_file = open('steem_posts.txt','wt')
        # n = text_file.write(str(string))
        # text_file.close()

        # data = json.load(open('steem_posts.txt'))
        # pending_payouts.append(data['pending_payout_value'])
        # os.remove('steem_posts.txt')
    
    # print(pending_payouts)
    print(type(details))
    # # return 'You have clicked {} times. Input tags are {}, number of posts are {}'.format(clicks,tag,post)
    return str(dicts[0].keys())
    

if __name__ == "__main__":
    app.run_server(debug=True,port='8040')


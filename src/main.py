import dash
from dash.dependencies import Input,Output,State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_dangerously_set_inner_html as dds
import plotly.graph_objs as go

import os
from steem import Steem
from pick import pick
import pprint
import json

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


tab1 = dbc.Card(
    dbc.CardBody(
       
        [
        html.Div(
        style={'text-align':'center'},
        children=[
        html.H1('Post Details'),
        dcc.Input(id='tag',value="",className='text-area',placeholder='Enter Tags',disabled=False),
        html.Button('Get Data',id='button',className='button-css'),
        html.Div(
        style={'text-align':'center'},
        children=[  
            html.Iframe(id='output-text',className='output-class'),
        ]
        )]
    )
        ]))

optionsDict = {'Single Characteristic Comparison': ['Pending Payout Value', 'Total Pending Payout Value', 'Net Votes','Total Payout Value','Curator Payout Value'], 
                'Multiple Characteristic Comparison': ['Pending Payout vs Total Payout', 'Pending Payout vs Net Votes']}

names = list(optionsDict.keys())
nestedOptions = optionsDict[names[0]]

tab2 = dbc.Card(
    dbc.CardBody(
        [
        html.Div(
        style={'text-align':'center'},
        children=[
        dcc.Dropdown(id='option-select-two',
            className='option-select',
            placeholder='Select Operation',
            options=[{'label':name, 'value':name} for name in names],
            value = None),
        dcc.Dropdown(
            id='second-drop',
            className='option-select',
            placeholder='Select values to compare',
            disabled=True,
            multi=True
        ),
        html.Br(),
        dcc.Input(id='tag-two',value="",className='text-area',placeholder='Enter Tags',disabled=True),
        dcc.Input(id='posts-two',value="",className='text-area',placeholder='Enter Number of Posts',type='number',disabled=True),
        html.Button('Get Data',id='button-two',className='button-css'),
        ]
    ),
    dbc.Row(
        [
            dbc.Col(dcc.Graph(
                style={'width':'99%','height':'500px'},
                id='graphA'
            )),
            dbc.Col(dcc.Graph(
                style={'width':'99%','height':'500px'},
                id='graphB'
            ))
        ]
    ),
    dbc.Row(
        [
            dbc.Col(dcc.Graph(
                style={'width':'99%','height':'500px'},
                id='graphC'
            )),
            dbc.Col(dcc.Graph(
                style={'width':'99%','height':'500px'},
                id='graphD'
            ))
        ]
    )],
    style={'height':'1000px'}

    )
)


@app.callback(
    [Output('second-drop', 'options'),
     Output('second-drop','disabled')],
    [Input('option-select-two', 'value')]
)
def update_date_dropdown(name):
    if(name==None):
        return[ [],True ]
    else:    
        return [[{'label': i, 'value': i} for i in optionsDict[name]],False]




app.title = 'honeybee'
app.layout = html.Div(
     children=[
    dbc.Row([dbc.Col(dbc.Jumbotron(
        children=[
            html.H1('honeybee',style={'text-align':'left','margin-left':'50px'}),
            html.H2('The Hive Data Collector',style={'text-align':'left','margin-left':'50px'}),
        ],
    ))]),
    dbc.Row([dbc.Col(dbc.Tabs(
        [
            dbc.Tab(tab1, label="Get Post Details"),
            dbc.Tab(tab2, label="Post Analytics"),
            dbc.Tab(
                "This tab's content is never seen", label="Blockchain Info", disabled=True
            ),
        ],
    ),)]),
    html.Br(),
    dbc.Row([dbc.Col(dbc.Jumbotron(
        children=[
            html.H3('Made with <3 by fillerInk ',style={'text-align':'left','margin-left':'50px'}),
            html.H4('The Hive Data Collector',style={'text-align':'left','margin-left':'50px'}),
        ],
        fluid=True,
        # style={'margin-bottom':'-20px','margin-top':'100px'}
        #className='fixed-bottom'
    ))]),
     ],
)

@app.callback(
    [Output(component_id='tag-two',component_property='disabled'),
    Output(component_id='posts-two',component_property='disabled')],
    [Input(component_id='option-select-two',component_property='value')]
)
def option_select_tab2(val):
    if(val=='Single Characteristic Comparison'):
        return False,False
    
    elif(val=='Multiple Characteristic Comparison'):
        return False,True
    
    else:
        return True,True

@app.callback(
    Output(component_id='output-text',component_property='srcDoc'),    
    [Input(component_id='button',component_property='n_clicks')],
    state=[State(component_id='tag',component_property='value')]
    )
def updatePostInformation(clicks,tag):
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
    

@app.callback(
    [Output(component_id='graphA',component_property='figure'),
    Output(component_id='graphB',component_property='figure'), 
    Output(component_id='graphC',component_property='figure'), 
    Output(component_id='graphD',component_property='figure')] ,  
    [Input(component_id='button-two',component_property='n_clicks')],
    state=[State(component_id='option-select-two',component_property='value'),
    State(component_id='second-drop',component_property='value'),
    State(component_id='tag-two',component_property='value'),
    State('posts-two','value')]
    )
def updateGraphs(clicks,option,suboption,tag,post):

    print(option)
    print(suboption)

    if (option=='Single Characteristic Comparison'):
        s = Steem()
        print('ivide kerii')
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

        char1 = []
        char2 = []
        char3 = []
        char4 = []

        #list_of_characteristics = [char1,char2,char3,char4]
        
        
        # for post in dicts:
        #     # char1.append(post[suboption[0]])
        #     # char2.append(post[suboption[1]])
        #     # char3.append(post[suboption[2]])
        #     # char4.append(post[suboption[3]])
        #     for i in range(len(suboption)):
        #         list_of_characteristics[i].append(suboption[i])
        # #print(type(pending[0]))
        # y1 = []
        # y2 = []
        # y3 = []
        # y4 = []

        # list_of_y = [y1,y2,y3,y4]

        # for i in range(len(list_of_characteristics)):
        #     for entry in list_of_characteristics[i]:
        #         for word in entry.split():
        #             print(word)
        #             try:
        #                 list_of_y[i].append(float(word))
        #             except:
        #                 print()

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
    
        x = []
        for i in range(len(post)):
            x.append(i)
        
        x = []
        for i in range(post):
            print(i)
            x.append(i)
        
        # datum1 = []
        # trace1 = go.Scatter(x=x,y=list_of_y[0],name=suboption[0],line=dict(color='#f44242'))
        # datum1.append(trace1)

        # datum2 = []
        # trace2 = go.Scatter(x=x,y=list_of_y[1],name=suboption[1],line=dict(color='#f44242'))
        # datum2.append(trace2)

        # datum3 = []
        # trace3 = go.Scatter(x=x,y=list_of_y[2],name=suboption[2],line=dict(color='#f44242'))
        # datum3.append(trace3)

        # datum4 = []
        # trace4 = go.Scatter(x=x,y=list_of_y[3],name=suboption[3],line=dict(color='#f44242'))
        # datum4.append(trace4)

        # layouts1 = {'title':suboption[0]}
        # layouts2 = {'title':suboption[1]}
        # layouts3 = {'title':suboption[2]}
        # layouts4 = {'title':suboption[3]}

        # result1 = {
        #     "data" : datum1,
        #     "layout" : layouts1
        # }
        # result2 = {
        #     "data" : datum2,
        #     "layout" : layouts2
        # }
        # result3 = {
        #     "data" : datum3,
        #     "layout" : layouts3
        # }
        # result4 = {
        #     "data" : datum4,
        #     "layout" : layouts4
        # }

        # finallist = []

        # finallist.append(result1)
        # finallist.append(result2)
        # finallist.append(result3)
        # finallist.append(result4)
        # print(finallist)
        # return finallist
        return 


    elif(option=='Multiple Characteristic Comparison'):

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
        
        x = []
        for i in range(len(post)):
            x.append(i)
        
        datum = []
        trace = go.Scatter(x=x,y=numbers,name='Pending Payouts',line=dict(color='#f44242'))

        datum.append(trace)

        layouts = {'title':'Pending Payouts'}
        
        return {
            "data" : datum,
            "layout" : layouts
        } 


   
if __name__ == "__main__":
    app.run_server(debug=True,port='8040')


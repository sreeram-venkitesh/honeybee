import dash
from dash.dependencies import Input,Output,State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import flask
from random import randint
import os
import os
from steem import Steem
from pick import pick
import pprint
import json


server = flask.Flask(__name__)
server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))
app = dash.Dash(__name__,server=server,external_stylesheets=[dbc.themes.BOOTSTRAP])


tab1 = dbc.Card(
    dbc.CardBody(
       
        [
        html.Div(
        style={'text-align':'center','background':'#f0f0f8'},
        children=[
        html.H1('Post Details'),
        dcc.Input(id='tag',value="",className='text-area',placeholder='Enter Tags',disabled=False),
        html.Button('Get Data',id='button',className='button-css'),
        html.Br(),
        html.Div(
        style={'text-align':'center'},
        children=[  
            html.Iframe(id='output-text',className='output-class',style={
                'width':'100%','height':'1000px'
            }),
        ]
        )]
    )
        ]),style={'background':'#f0f0f8','height':'100%'})

optionsDict = {'Single Characteristic Comparison': ['pending_payout_value', 'total_pending_payout_value', 'net_votes','total_payout_value','curator_payout_value'], 
                'Multiple Characteristic Comparison': ['Pending Payout vs Total Payout', 'Pending Payout vs Net Votes']}

names = list(optionsDict.keys())
nestedOptions = optionsDict[names[0]]

tab2 = dbc.Card(
    dbc.CardBody(
        [
        html.Div(
        style={'text-align':'center','background':'#f0f0f8'},
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
        html.Br()
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
        ],
        style={'background':'#f0f0f8'}
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

    ),style={'background':'#f0f0f8'}
    
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
    
    dbc.Row([
        dbc.Col(dbc.Jumbotron(
        children=[

            html.H1('honeybee',style={'text-align':'left','margin-left':'50px','color':'#212529','font-weight':'bold'}),
            html.Hr(),
            html.H2('The Hive Data Collector',style={'text-align':'left','margin-left':'50px','color':'#212529'}),
        ],
        style={'background':'#E31337','padding-right':'0px'},
        fluid=True
        ),
        style={'padding-right':'0px'}),
        dbc.Col(
            dbc.Jumbotron(
        children=[

            
            html.H1(html.A('GitHub',href='https://github.com/fillerink/honeybee'),style={'text-align':'right','padding-right':'30px'}),
            html.Hr(),
            html.H2("STEEMGeek Hackathon",style={'text-align':'right','padding-right':'30px'})
        ],
        style={'background':'#E31337'},
        fluid=True
        ),style={'margin-left':'0px','padding-left':'0px'}
        )
    
    ],style={'margin-bottom':'0px'}),

    dbc.Row([dbc.Col(dbc.Tabs(
        [
            dbc.Tab(tab1, label="Get Post Details"),
            dbc.Tab(tab2, label="Post Analytics"),
            dbc.Tab(
                "This tab's content is never seen", label="Blockchain Info", disabled=True
            ),
        ],style={'background':'#e7e7f1'}
    ),style={'background':'#e7e7f1'})],style={'background':'#e7e7f1'}),
    

    ],style={'background':'#e7e7f1'}
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
        return False,False
    
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
    post_info = "Post Info <br><br>Author : {} <br><br>Category : {} <br><br>Created : {} <br><br>Title : {} <br><br> Total Votes : {} <br><br>Pending Payout Value : {} <br><br>Total Pending Payout Value : {} <br><br>Body : {} ".format(dicts[0]['author'],
        dicts[0]['category'],dicts[0]['created'],dicts[0]['title'],dicts[0]['net_votes'],dicts[0]['pending_payout_value'],dicts[0]['total_pending_payout_value'],dicts[0]['body'])
    #print(post_info)
    #return str(dicts[0].keys())
    return post_info
    

@app.callback(
    [Output(component_id='graphA',component_property='figure'),
    Output(component_id='graphB',component_property='figure'), 
    Output(component_id='graphC',component_property='figure'), 
    Output(component_id='graphD',component_property='figure')
    ] ,  
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

        list_of_characteristics = [char1,char2,char3,char4]
        
        
        for post in dicts:
            for i in range(len(suboption)):
                list_of_characteristics[i].append(post[suboption[i]])
        #print(type(pending[0]))
        y1 = []
        y2 = []
        y3 = []
        y4 = []

        if len(suboption) == 1:
            suboption.append("empty")
            suboption.append("empty")
            suboption.append("empty")
        elif len(suboption) == 2:
            suboption.append("empty")
            suboption.append("empty")
        elif len(suboption) == 3:
            suboption.append("empty")

        print(suboption)

        list_of_y = [y1,y2,y3,y4]

        print('list of characteristics ' +str(list_of_characteristics))
        for i in range(len(list_of_characteristics)):
            
            for entry in list_of_characteristics[i]:
                #print('entry len'+str(len(entry)))
                print('entry type '+str(type(entry)))
                if(type(entry)==int):
                    list_of_y[i].append(entry)
                else:
                    for word in entry.split():
                        print(word)
                        try:
                            list_of_y[i].append(float(word))
                        except:
                            print('int aano nokkuna stage ethy')
                            
        x = []
        for i in range(len(posts)): 
            x.append(i)
        print(x)
        
        print(list_of_y[0])
        print(list_of_y[1])
        print(list_of_y[2])
        print(list_of_y[3])
        
        print('first stage printed, going to second')
        for i in range (0,4):
            if (len(list_of_y[i]) == 0):
                list_of_y[i] = [0,0,0,0] 
        
        
        print('nammade initialisation complete')
        print(list_of_y[0])
        print(list_of_y[1])
        print(list_of_y[2])
        print(list_of_y[3])

 
        datum1 = []
        trace1 = go.Scatter(x=x,y=list_of_y[0],name=suboption[0],line=dict(color='#f44242'))
        datum1.append(trace1)

        datum2 = []
        trace2 = go.Scatter(x=x,y=list_of_y[1],name=suboption[1],line=dict(color='#f44242'))
        datum2.append(trace2)

        datum3 = []
        trace3 = go.Scatter(x=x,y=list_of_y[2],name=suboption[2],line=dict(color='#f44242'))
        datum3.append(trace3)

        datum4 = []
        trace4 = go.Scatter(x=x,y=list_of_y[3],name=suboption[3],line=dict(color='#f44242'))
        datum4.append(trace4)

        layouts1 = {'title':suboption[0]}
        layouts2 = {'title':suboption[1]}
        layouts3 = {'title':suboption[2]}
        layouts4 = {'title':suboption[3]}

        result1 = {
            "data" : datum1,
            "layout" : layouts1
        }
        result2 = {
            "data" : datum2,
            "layout" : layouts2
        }
        result3 = {
            "data" : datum3,
            "layout" : layouts3
        }
        result4 = {
            "data" : datum4,
            "layout" : layouts4
        }

        finallist = []

        finallist.append(result1)
        finallist.append(result2)
        finallist.append(result3)
        finallist.append(result4)
        #print(finallist)
        print('net votes: ' + str(list_of_y[1]))
        
        return finallist
         


    elif(option=='Multiple Characteristic Comparison'):

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
        
        return [{
            "data" : datum,
            "layout" : layouts
        },{},{},{}] 


   
if __name__ == "__main__":
    app.run_server(debug=False,port='8030')


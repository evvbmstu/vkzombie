# -*- coding: utf-8 -*-
from flask import Flask, request, json, jsonify
from settings import *
import vk
import sys
import json
import handlers
import dash
#import pandas as pd
#import dash_core_components as dcc
#import dash_html_components as html
#import plotly.graph_objs as go

app = Flask( __name__ )
#dashapp = dash.Dash ( __name__, server = app )


@app.route("/poll", methods = ['POST'])
def processing():
    newJson = request.get_json()
    if "type" in newJson.keys():
        if newJson['type'] == "message_new":
                session = vk.Session()
                api = vk.API( session )
                user_id = newJson['object']['user_id']
                text = newJson['object']['body'].encode("utf8")
                answer = handlers.handler( text, user_id )
		print( answer )
		api.messages.send( access_token = token, 
				   user_id = str(user_id), 
			           message = answer )
                return 'ok'
        elif newJson['type'] == "confirmation":
                return '9f3fba60'



#df = pd.read_csv(
#    'https://gist.githubusercontent.com/chriddyp/' +
#    '5d1ea79569ed194d432e56108a04d188/raw/' +
#    'a9f9e8076b837d541398e999dcbac2b2826a81f8/'+
#    'gdp-life-exp-2007.csv')#
#
#
#dashapp.layout = html.Div([
#    dcc.Graph(
#        id='life-exp-vs-gdp',
#        figure={
#            'data': [
#                go.Scatter(
#                    x=df[df['continent'] == i]['gdp per capita'],
#                    y=df[df['continent'] == i]['life expectancy'],
#                    text=df[df['continent'] == i]['country'],
#                    mode='markers',
#                    opacity=0.7,
#                    marker={
#                        'size': 15,
#                        'line': {'width': 0.5, 'color': 'white'}
#                    },
#                    name=i
#                ) for i in df.continent.unique()
#            ],
#            'layout': go.Layout(
#                xaxis={'type': 'log', 'title': 'GDP Per Capita'},
#                yaxis={'title': 'Life Expectancy'},
#                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
#                legend={'x': 0, 'y': 1},
#                hovermode='closest'
#            )
#        }
#    )
#])
#
#
if __name__ == "__main__":
    app.run()

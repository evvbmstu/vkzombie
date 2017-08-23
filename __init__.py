# -*- coding: utf-8 -*-
from flask import Flask, request, json, jsonify
from settings import *
import vk
import sys
import json
import handlers

app = Flask(__name__)
@app.route("/poll", methods = ['POST'])
def processing():
    newJson = request.get_json()
    if "type" in newJson.keys():
        if newJson['type'] == "message_new":
                session = vk.Session()
                api = vk.API( session )
                user_id = newJson['object']['user_id']
                text = newJson['object']['body'].encode("utf8")
                answer = handlers.handler( text )
                api.messages.send( access_token = token, 
				   user_id = str(user_id), 
			           message = answer )
                return 'ok'
        elif newJson['type'] == "confirmation":
                return '9f3fba60'
    else:
        return jsonify ( {"pasha":"privet"} )
if __name__ == "__main__":
    app.run()

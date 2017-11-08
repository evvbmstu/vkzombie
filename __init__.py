# -*- coding: utf-8 -*-
from flask import Flask, request, json, jsonify
from settings import *
import vk
import sys
import json
import handlers
import jsonpickle
import numpy as np
import cv2
app = Flask( __name__ )

@app.route("/poll", methods = ['POST'])
def processing():
    newJson = request.get_json()
    if "type" in newJson.keys():
        if newJson['type'] == "message_new":
                session = vk.Session()
                api = vk.API( session )
                user_id = newJson['object']['user_id']
                text = newJson['object']['body'].encode("utf8")
	 	try:
                    answer = handlers.handler( text, user_id )
	 	except:
		    answer = " Упс, что-то пошло не так. Ребята с ИУ уже разбираются. Не обижайтесь, это всё таки бета тест. Возможно вы что-то сделали не так, еще раз почитайте команды )  "
		#print( answer )
		if answer[0] == 'p':
		    api.messages.send( access_token = token,
				       user_id = str(user_id),
			               message = "Расписание спорткомплекса",
				       attachment = SPORT_PHOTOS )
		else:
		    api.messages.send( access_token = token, 
				       user_id = str(user_id), 
			               message = answer )
                return 'ok'
        elif newJson['type'] == "confirmation":
                return '9f3fba60'

@app.route("/video_test", methods = ['POST'])
def video_test():
    r = request
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # do some fancy processing here....

    # build a response dict to send back to client
    response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])
                }
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")

if __name__ == "__main__":
    app.run()

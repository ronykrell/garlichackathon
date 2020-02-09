#!/usr/bin/env python

from flask import Flask, request, redirect, url_for
from flask_restful import Resource, Api
from joblib import load
import numpy as np
import pandas as pd
import sklearn
import json
import asyncio
import websockets
import logging

import time


logging.basicConfig()

STATE = {"value": 0}

USERS = set()


def state_event():
    return json.dumps({"type": "state", **STATE})


def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})


async def notify_new_data(data):
    if USERS:  # asyncio.wait doesn't accept an empty list
        json_data = json.dumps(data)
        await asyncio.wait([user.send(json_data) for user in USERS])


async def notify_users():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def register(websocket):
    USERS.add(websocket)
    await notify_users()


async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()

#
# async def counter(websocket, path):
#     # register(websocket) sends user_event() to websocket
#     await register(websocket)
#     try:
#         await websocket.send(state_event())
#         async for message in websocket:
#             data = json.loads(message)
#             if data["action"] == "minus":
#                 STATE["value"] -= 1
#                 await notify_state()
#             elif data["action"] == "plus":
#                 STATE["value"] += 1
#                 await notify_state()
#             else:
#                 logging.error("unsupported event: {}", data)
#     finally:
#         await unregister(websocket)






















from flask_cors import CORS, cross_origin

# Upload folder
UPLOAD_FOLDER = 'img'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)

#
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['CORS_HEADERS'] = 'Content-Type'
# CORS(app)
#
# api = Api(app)

latest_pred = 0
latest_actual = 0


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_prediction(feature_row):
    json_row = json.loads(feature_row)
    features_array = json_row['feature_row'][:10]
    actual_movement = json_row['feature_row'][-1]
    np_arr = np.array(features_array).reshape(1,-1)
    prediction = model.predict(np_arr)[0]
    print(prediction)
    print("Ran prediction")
    return {"pred": prediction, "actual": actual_movement}


global global_latest_pred
global global_latest_actual
global global_history
global model

model = load("trained_classifier.joblib")



global_latest_pred = 0
global_latest_actual = 0
global_history = []


class MovementPrediction(Resource):

    def post(self):
        feature_row = request.get_json()
        print(feature_row)
        pred_obj = get_prediction(feature_row)
        global_latest_pred = pred_obj['pred']
        global_latest_actual = pred_obj['actual']
        global_history.append({'pred':  global_latest_pred, 'actual': global_latest_actual})
        print("Added point")
        print(len(global_history))
        return {'success': "True"}

    def get(self):
        ind_json = request.args.get('index')
        print(ind_json)
        ind_num = int(ind_json)
        print(ind_num)
        if len(global_history) < ind_num + 1:
            return {"success": "False"}
        else:
            return global_history[ind_num]


# api.add_resource(MovementPrediction, '/predict/')


# WS server example

async def hello(websocket, path):
    name = await websocket.recv()
    print(f"< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f"> {greeting}")


async def save_the_data(message):
    # feature_row = await websocket.recv()
    feature_row = message
    print(feature_row)
    pred_obj = get_prediction(feature_row)
    global_latest_pred = pred_obj['pred']
    global_latest_actual = pred_obj['actual']
    global_history.append({'pred': global_latest_pred, 'actual': global_latest_actual})
    print("Added point")
    print(len(global_history))
    # print("Got")
    # print(f"< {name}")
    # await websocket.send("Got it")
    # print(f"> {greeting}")


async def save_data(websocket, path):
    try:
        delay = 0
        await register(websocket)
        async for message in websocket:
            if message == "slow":
                delay = .5
            else:
                await save_the_data(message)
                time.sleep(delay)
                await notify_new_data(global_history[-1])
    finally:
        await unregister(websocket)





print("Im alive")

start_server = websockets.serve(save_data, "localhost", 8765, ping_timeout=None)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()



# if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0')


logging.basicConfig()

STATE = {"value": 0}

USERS = set()


def state_event():
    return json.dumps({"type": "state", **STATE})


def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})


async def notify_state():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = state_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def notify_users():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def register(websocket):
    USERS.add(websocket)
    await notify_users()


async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()


async def counter(websocket, path):
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    try:
        await websocket.send(state_event())
        async for message in websocket:
            data = json.loads(message)
            if data["action"] == "minus":
                STATE["value"] -= 1
                await notify_state()
            elif data["action"] == "plus":
                STATE["value"] += 1
                await notify_state()
            else:
                logging.error("unsupported event: {}", data)
    finally:
        await unregister(websocket)


start_server = websockets.serve(counter, "localhost", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()



















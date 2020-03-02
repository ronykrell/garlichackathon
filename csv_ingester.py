#!/usr/bin/env python

from flask import Flask, request, redirect, url_for
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename
import os
import numpy as np
import json
import urllib3
import asyncio
import websockets
import time
async def send_to_server():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        counter = 0
        while True:
            if counter == 0:
                print("in send to server")
                data = np.loadtxt("merged_data.csv", delimiter=',')
                np.random.shuffle(data)
                for data_point in data:
                    counter = counter + 1
                    # if counter == 10:
                    #     break

                    print(data_point)
                    # pred_result = get_prediction(json.dumps({'features': data_point.tolist()}))

                    # latest_pred = pred_result['pred']
                    # latest_actual = pred_result['actual']

                    b = data_point.tolist()
                    # # json_datapoint = json.dump(b, indent=4)  ### this saves the array in .json format
                    encoded_body = json.dumps({'feature_row': b})
                    print(counter)
                    #
                    # http = urllib3.PoolManager()
                    #
                    # http.request('POST', 'http://localhost:5000/predict/',
                    #              headers={'Content-Type': 'application/json'},
                    #              body=encoded_body)

                    await websocket.send(encoded_body)
                    # status = await websocket.recv()

                    # print("Se")
                    print("Sent datapoint to server")




                # name = input("What's your name? ")
                # name = "Rony"
                #
                #
                # greeting = await websocket.recv()
                # print(f"< {greeting}")



# WS client example

async def hello():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        # name = input("What's your name? ")
        name = "Rony"
        await websocket.send(name)
        print(f"> {name}")

        greeting = await websocket.recv()
        print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(send_to_server())
















#!/usr/bin/env python3.7

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS, cross_origin
from threading import Thread
from bluepy import btle

import binascii
import json
import time
import os

import status

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'cleSecrete'
app._static_folder = os.path.abspath("templates/static/")

thread = None
data_ble = [b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00']
mower = None

class MyDelegate(btle.DefaultDelegate):
    def __init__(self,params):
        btle.DefaultDelegate.__init__(self)
    def handleNotification(self,cHandle,data):
        global data_ble
        for i in range(0,19):
            data_ble[i] = binascii.b2a_hex(data[i:(i+1)])

def back_thread():
        global mower
        mower = btle.Peripheral('50:33:8B:F8:5A:90')
        mower.setDelegate(MyDelegate(0))
        while True:
            mower.waitForNotifications(1)
            i = 1

@app.route('/') 
def sessions():
        global thread
        if thread is None:
                thread = Thread(target=back_thread)
                thread.start()
        return render_template("index.html")

@app.route('/ble', methods=['GET', 'POST'])
def ble():
    if request.method == 'GET':
        print("ble")
        print(data_ble)
        data_json = status.decodeReceivedData(data_ble)
        print("json")
        print(data_json)
        return jsonify(data_json)

    if request.method == 'POST':
        print(request.get_json())  # parse as JSON
        return jsonify(status=200)

@app.route('/start', methods=['POST'])
def commandStart():
    if request.method == 'POST':
        print(request.get_json())  # parse as JSON

        mowerService = mower.getServiceByUUID("0000ffe0-0000-1000-8000-00805f9b34fb")
        mowerCharac = mowerService.getCharacteristics()[0]

        mowerCharac.write(bytes('1', 'utf-8'))

        return jsonify(status=200)

@app.route('/stop', methods=['POST'])
def commandStop():
    if request.method == 'POST':
        print(request.get_json())  # parse as JSON

        mowerService = mower.getServiceByUUID("0000ffe0-0000-1000-8000-00805f9b34fb")
        mowerCharac = mowerService.getCharacteristics()[0]

        mowerCharac.write(bytes('2', 'utf-8'))

        return jsonify(status=200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


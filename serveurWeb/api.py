#!/usr/bin/env python3.7
# app/socket.py
from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit
from threading import Thread
from bluepy import btle

import binascii
import struct
import json
import time
import os

import status

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'cleSecrete'
app._static_folder = os.path.abspath("templates/static/")
socketio = SocketIO(app)
socketio.init_app(app)

thread = None
data_ble = [b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00']

class MyDelegate(btle.DefaultDelegate):
    def __init__(self,params):
        btle.DefaultDelegate.__init__(self)
    def handleNotification(self,cHandle,data):
        global data_ble
        for i in range(0,17):
            data_ble[i] = binascii.b2a_hex(data[i:(i+1)])
##        print(data_ble)


def back_thread():
        mower = btle.Peripheral('50:33:8B:F8:5A:90')
        mower.setDelegate(MyDelegate(0))
        while True:
            mower.waitForNotifications(1)
            data_json = status.decodeReceivedData(data_ble)
##            print(data_json)
            socketio.emit('message', data_json)

@app.route('/') 
def sessions():
        global thread
        if thread is None:
                thread = Thread(target=back_thread)
                thread.start()
        return render_template("index.html")

@socketio.on('command')
def get_start_command(json, methods=['GET']):
    print("event")
    print(str(json))

if __name__ == '__main__':
#       app.run()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

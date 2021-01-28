#! /usr/bin/env python3
# app/socket.py
from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit
from threading import Thread

import json
#import serial
import time
import os
import status

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'cleSecrete'
app._static_folder = os.path.abspath("templates/static/")
socketio = SocketIO(app)
thread = None


statusMower = 0x08
receivedData = 0x09
#serialBle = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=1)
#serialBle.flush();

def read_json():
	with open('status.json') as json_read:
		data_dict = json.load(json_read)
	return data_dict

def write_json(data_dict):
	with open('status.json', 'w') as json_write:
		json.dump(data_dict, json_write)

def back_thread():
	data = read_json()
	while True:
		print("while loop")
		#if serialBle.in_waiting > 0:
		#	status = serialBle.readline()
		#	receivedData = serialBle.readline()
		data_status = status.decodeReceivedData(statusMower, receivedData)
		data.update(data_status)
		print(data)
		socketio.emit('message', data)
		time.sleep(3)

@app.route('/')	
def sessions():
	global thread
	if thread is None:
		thread = Thread(target=back_thread)
		thread.start()
	print("appel index")
	return render_template("index.html")

@socketio.on('command')
def get_start_command(json, methods=['GET']):
	print(str(json))

if __name__ == '__main__':
#	app.run()
	socketio.run(app, host='0.0.0.0', debug=True)

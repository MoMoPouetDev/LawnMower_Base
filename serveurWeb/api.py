#!/usr/bin/env python3.7

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS, cross_origin
from flask_mqtt import Mqtt
from threading import Thread
from bluepy import btle
from gpiozero import Button, LED
from logging.handlers import RotatingFileHandler

import paho.mqtt.client as mqtt
import binascii
import json
import time
import os
import datetime
import logging

import status

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
file_handler = RotatingFileHandler('activity.log', 'a', 1000000, 1)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'cleSecrete'
app._static_folder = os.path.abspath("templates/static/")

broker_address="192.168.1.108"
mqtt.Client.connected_flag=False

led_IR = LED(3)
button_IR = Button(5)

thread = None
data_ble = [b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00']
mower = None
client = None
flagBleDisconnect = False
flagMqttDisconnect = False
flagMqttReceived = False

class MyDelegate(btle.DefaultDelegate):
    def __init__(self,params):
        btle.DefaultDelegate.__init__(self)
    def handleNotification(self,cHandle,data):
        global data_ble
        for i in range(0,19):
            data_ble[i] = binascii.b2a_hex(data[i:(i+1)])

def back_thread():
    global flagBleDisconnect
    global flagMqttReceived

    test = 0
    led_IR.on()    

    connect_mower()
    mower.setDelegate(MyDelegate(0))
    while True:
        test = test + 1
        try:
            if mower.waitForNotifications(0.5):
                logger.debug("BLE Connected")
                client.publish("PUBmower",test)
                flagBleDisconnect = False
                flagMqttReceived = False
                continue
        except btle.BTLEDisconnectError:
            logger.debug("BLE Disconnected")
            flagBleDisconnect = True
            return back_thread()
        if button_IR.is_pressed:
            print("pressed")
        else:
            print("not pressed")

def connect_mower():
    global mower
    global thread
    try:
        mower = btle.Peripheral('50:33:8B:F8:5A:90')
    except Exception as e:
        logger.error("Connection Error",e)
        thread = None 
        return launch_thread()

def decode_data_ble():
    return status.decodeReceivedData(data_ble)

def send_command_ble(command):
    mowerService = mower.getServiceByUUID("0000ffe0-0000-1000-8000-00805f9b34fb")
    mowerCharac = mowerService.getCharacteristics()[0]

    mowerCharac.write(bytes(command, 'utf-8'))

def launch_thread():
    global thread
    thread = Thread(target=back_thread)
    thread.start()

def stop_thread():
    thread.join()

def on_connect_mqtt(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True
        logger.debug("connected OK")
    else:
        logger.error("Bad connection Returned code=",rc)

def on_message_mqtt(client, userdata, message):
    global flagMqttReceived
    command = str(message.payload.decode("utf-8"))
    print("message received " ,command)
    flagMqttReceived = True 
    if command=="start" and not flagMqttReceived:
        send_command_ble('1')
    if command=="stop" and not flagMqttReceived:
        send_command_ble('2')

def start_mqtt():
    global client
    
    client = mqtt.Client()
    client.on_connect = on_connect_mqtt
    client.on_message = on_message_mqtt
    client.connect(broker_address, 1883)
    client.loop_start()
    
    while not client.connected_flag:
        logger.debug("Wait")
        time.sleep(1)
    
    client.subscribe("SUBmower")    

def stop_mqtt():
    client.loop_stop()
    client.disconnect()

@app.route('/') 
def sessions():
    if thread is None:
        launch_thread()
    return render_template("index.html")

@app.route('/ble', methods=['GET', 'POST'])
def ble():
    if request.method == 'GET':
        if flagBleDisconnect == True:
            logger.debug("BLE Disconnected")
            return jsonify(connection="Error")

        if flagBleDisconnect == False:
            data_json = decode_data_ble()
            logger.debug("JSON ",data_json)
            return jsonify(data_json)

    if request.method == 'POST':
        logger.debug(request.get_json())  # parse as JSON
        return jsonify(status=200)

@app.route('/start', methods=['POST'])
def commandStart():
    if request.method == 'POST':
        logger.debug(request.get_json())  # parse as JSON
        send_command_ble('1')
        return jsonify(status=200)

@app.route('/stop', methods=['POST'])
def commandStop():
    if request.method == 'POST':
        logger.debug(request.get_json())  # parse as JSON
        send_command_ble('2')
        return jsonify(status=200)

start_mqtt()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


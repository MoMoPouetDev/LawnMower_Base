#! /usr/bin/python

import time
import json

from enum import Enum

class StatusMower(Enum):
	UNKNOWN_ETAT = 0x00
	TACHE_EN_COURS = 0x01
	RETOUR_STATION = 0x02
	EN_CHARGE = 0x03
	PAS_DE_TACHE_EN_COURS = 0x04
	PAUSE = 0x05
	
class ErrorMower(Enum):
	NTR = 0x08
	BLOCKED_MOWER = 0x09
	DETECTED_RAIN = 0x0A
	WIRE_NOT_DETECTED = 0x0B
	LOW_BATTERY = 0x0C
	VERY_LOW_BATTERY = 0x0D
	EMPTY_BATTERY = 0x0E
	
class Command(Enum):
	START = 0x11
	STOP = 0x12
	FORCE_START = 0x13
	
def decodeReceivedData(status, receivedData):
	if status == 0x00:
		if StatusMower(receivedData) == StatusMower.UNKNOWN_ETAT:
			etatMower = "UNKNOWN_ETAT"
		elif StatusMower(receivedData) == StatusMower.TACHE_EN_COURS:
			etatMower = "TACHE_EN_COURS"
		elif StatusMower(receivedData) == StatusMower.RETOUR_STATION:
			etatMower = "RETOUR_STATION"
		elif StatusMower(receivedData) == StatusMower.EN_CHARGE:
			etatMower = "EN_CHARGE"
		elif StatusMower(receivedData) == StatusMower.PAS_DE_TACHE_EN_COURS:
			etatMower = "PAS_DE_TACHE_EN_COURS"
		elif StatusMower(receivedData) == StatusMower.PAUSE:
			etatMower = "PAUSE"
		return {"status": etatMower}
		
	elif status == 0x08:
		if ErrorMower(receivedData) == ErrorMower.NTR:
			errorMower = "NTR"
		elif ErrorMower(receivedData) == ErrorMower.BLOCKED_MOWER:
			errorMower = "BLOCKED_MOWER"
		elif ErrorMower(receivedData) == ErrorMower.DETECTED_RAIN:
			errorMower = "DETECTED_RAIN"
		elif ErrorMower(receivedData) == ErrorMower.WIRE_NOT_DETECTED:
			errorMower = "WIRE_NOT_DETECTED"
		elif ErrorMower(receivedData) == ErrorMower.LOW_BATTERY:
			errorMower = "LOW_BATTERY"
		elif ErrorMower(receivedData) == ErrorMower.VERY_LOW_BATTERY:
			errorMower = "VERY_LOW_BATTERY"
		elif ErrorMower(receivedData) == ErrorMower.EMPTY_BATTERY:
			errorMower = "EMPTY_BATTERY"
		return {"error": errorMower}
			
			

if __name__ == '__main__':
	#serialBle = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=1)
	#serialBle.flush();
	
	#while True:
	#	if ser.in_waiting > 0:
	#		status = serialBle.readline()
	#		receivedData = serialBle.readline()
	#		decodeReceivedData(status, receivedData)
	#		
	#	if dataToSend:
	#		serialBle.write(data)
	
	status = 0x08
	receivedData = 0x0D
	test = decodeReceivedData(status, receivedData)
	print(test)
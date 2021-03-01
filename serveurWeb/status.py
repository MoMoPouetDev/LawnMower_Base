#! /usr/bin/env python3.7
# status.py
import time
import json

from locale import atof
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
    
def decodeReceivedData(data_ble):
    data_json = read_json()
    etatMower = data_ble[0]
    res = decodeStatusMower(etatMower)
    data_json.update(res)

    errorMower = data_ble[1]
    res = decodeErrorMower(errorMower)
    data_json.update(res)

    batteryLevel = data_ble[2]
    res = decodeBatteryLevel(batteryLevel)
    data_json.update(res)
    
    latitudeDegrees = data_ble[3]
    latitudeMinutes = data_ble[4]
    latitudeMSB = data_ble[5]
    latitudeB = data_ble[6]
    latitudeLSB = data_ble[7]
    res = decodeLatitude(latitudeDegrees, latitudeMinutes, latitudeMSB, latitudeB, latitudeLSB)
    data_json.update(res)
    
    longitudeDegrees = data_ble[8]
    longitudeMinutes = data_ble[9]
    longitudeMSB = data_ble[10]
    longitudeB = data_ble[11]
    longitudeLSB = data_ble[12]
    res = decodeLongitude(longitudeDegrees, longitudeMinutes, longitudeMSB, longitudeB, longitudeLSB)
    data_json.update(res)
   
    hoursGPS = data_ble[13]
    res = decodeHours(hoursGPS)
    data_json.update(res)

    minutesGPS = data_ble[14]
    res = decodeMinutes(minutesGPS)
    data_json.update(res)

    daysGPS = data_ble[15]
    res = decodeDays(daysGPS)
    data_json.update(res)

    monthsGPS = data_ble[16] 
    res = decodeMonths(monthsGPS)
    data_json.update(res)

    angleMSB = data_ble[17]
    angleLSB = data_ble[18]
    res= decodeAngle(angleMSB, angleLSB)
    data_json.update(res)

    write_json(data_json)

    return data_json

def decodeStatusMower(receivedData):
    receivedData = int(receivedData,16)
    if receivedData == StatusMower.UNKNOWN_ETAT.value:
        etatMower = "UNKNOWN_ETAT"
    elif receivedData == StatusMower.TACHE_EN_COURS.value:
        etatMower = "TACHE_EN_COURS"
    elif receivedData == StatusMower.RETOUR_STATION.value:
        etatMower = "RETOUR_STATION"
    elif receivedData == StatusMower.EN_CHARGE.value:
        etatMower = "EN_CHARGE"
    elif receivedData == StatusMower.PAS_DE_TACHE_EN_COURS.value:
        etatMower = "PAS_DE_TACHE_EN_COURS"
    elif receivedData == StatusMower.PAUSE.value:
        etatMower = "PAUSE"
    else:
        etatMower = "ERREUR"
    
    return {"status": etatMower}
        
def decodeErrorMower(receivedData):
    receivedData = int(receivedData,16)
    if receivedData == ErrorMower.NTR.value:
        errorMower = "NTR"
    elif receivedData == ErrorMower.BLOCKED_MOWER.value:
        errorMower = "BLOCKED_MOWER"
    elif receivedData == ErrorMower.DETECTED_RAIN.value:
        errorMower = "DETECTED_RAIN"
    elif receivedData == ErrorMower.WIRE_NOT_DETECTED.value:
        errorMower = "WIRE_NOT_DETECTED"
    elif receivedData == ErrorMower.LOW_BATTERY.value:
        errorMower = "LOW_BATTERY"
    elif receivedData == ErrorMower.VERY_LOW_BATTERY.value:
        errorMower = "VERY_LOW_BATTERY"
    elif receivedData == ErrorMower.EMPTY_BATTERY.value:
        errorMower = "EMPTY_BATTERY"
    else:
        errorMower = "ERREUR"
    
    return {"error": errorMower}
            
def decodeBatteryLevel(receivedData):
    batterieLevel = str(int(receivedData,16))
    return {"batterie": batterieLevel}

def decodeLatitude(latitudeDegrees, latitudeMinutes, latitudeMSB, latitudeB, latitudeLSB):
    latitudeDecimal = latitudeMSB + latitudeB + latitudeLSB
    tempLat = str(int(latitudeMinutes,16)) + "." + str(int(latitudeDecimal,16))
    latitude = str(float(int(latitudeDegrees,16)) + (atof(tempLat)/60.0))
    return {"latitude": latitude}

def decodeLongitude(longitudeDegrees, longitudeMinutes, longitudeMSB, longitudeB, longitudeLSB):
    longitudeDecimal = longitudeMSB + longitudeB + longitudeLSB
    tempLong = str(int(longitudeMinutes,16)) + "." + str(int(longitudeDecimal,16))
    longitude = str(float(int(longitudeDegrees,16)) + (atof(tempLong)/60.0))
    return {"longitude": longitude}

def decodeHours(hoursGPS):
    heures = str(int(hoursGPS,16))
    return {"heures": heures}

def decodeMinutes(minutesGPS):
    minutes = str(int(minutesGPS,16))
    return {"minutes": minutes}

def decodeDays(daysGPS):
    jours = str(int(daysGPS,16))
    return {"jours": jours}

def decodeMonths(monthsGPS):
    mois = str(int(monthsGPS,16))
    return {"mois": mois}

def decodeAngle(angleMSB, angleLSB):
    angle = str(int((angleMSB + angleLSB),16))
    return {"angle": angle}

def read_json():
    with open('status.json') as json_read:
        data_dict = json.load(json_read)
    return data_dict

def write_json(data_dict):
    with open('status.json','w') as json_write:
        json.dump(data_dict, json_write)        
    
if __name__ == '__main__':
    data_ble = [b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00',b'00']
    decodeReceivedData(data_ble)

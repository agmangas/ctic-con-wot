import network
from uStorage import Storage

class  configuration():
    def __init__(self):
        self.storage = Storage()

        # self.WIFI_SSID = "Heart_WiFi_AP"
        # self.WIFI_PASSWORD = "WiFiHEART2020"

        # self.WIFI_SSID = "Meteo"
        # self.WIFI_PASSWORD = "L1ke4Hurr1cane"

        # self.WIFI_SSID = "FiWi"
        # self.WIFI_PASSWORD = "Jedwqfe!21"

        self.WIFI_SSID = "Movil"
        self.WIFI_PASSWORD = "santi_123456"

        self.OTA_server_IP = "192.168.1.100"
        self.OTA_server_Port = 7772

        self.broker = "iot.eclipse.org"

        self.type = "saref:HVAC"
        self.context="http://purl.org/heart/context.jsonld"


        self.location = "IT" #IT: Italy, FR: France
        self.family = "SmartFancoil"# types: DHWBoiler, SmartFancoil, SmartRadiator
        self.number = self.storage.get_Value("ID")

        self.name = "{}-{}-{}-{}"
        self.id = "stille:{}:{}:{}:{}"
        self.description = "Location: {}, Type: {}, Number: {}, IP: {}. This is a Smart fancoil, it provides heat or cooling depeding on the room parameters. Version {}"


"""
#Code to reset filesystem

import uos
import pycom

pycom.bootmgr(fs_type=pycom.LittleFS, reset=True)

import uos
uos.fsformat("/flash")

"""

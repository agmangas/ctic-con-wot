import json
import logging
import os
import random
from time import sleep

from paho.mqtt import client as mqtt_client

#In this project we dont use this path! (We are creating client using environment)
config_file_path = os.path.abspath(os.path.join("common_modules", "mqttClient","config.json"))

# Class
class MqttClient():
    # Constructor
    def __init__(self, *args, **kwargs) -> None:
        try:
            print(kwargs)
            client_id = kwargs.pop('client_id') + str(random.randint(0, 1000))
            self.broker = kwargs.pop('broker')
            self.port = kwargs.pop('port')
            self.transport = kwargs.pop('transport')
            self.client_id = client_id

        except KeyError:
            logging.error("Not all parameters were passed")
            exit(1)

        except Exception as e:
            logging.error(f"Exception not controlled: {e}")

        self.topics = kwargs.pop('topics', [])
        self.isAnonymous = kwargs.pop('isAnonymous', True)
        if(self.isAnonymous):
            self.username = kwargs['credentials']['username']
            self.password = kwargs['credentials']['password']

        # Set Connecting Client ID
        self._client = mqtt_client.Client(self.client_id, transport=self.transport)

        return

    # Functions
    def connect(self, topic_to_subscribe=None):
        '''Connect and subscribe to topic (or topics) pass as parameter (If topic_to_subscribe is none, will subscribe to all the topics inside config.json file)'''
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                logging.info("Connected to MQTT Broker!")
            else:
                logging.warning("Failed to connect, return code %d\n", rc)

        try:
            logging.info("Lets connect to MQTT Broker!")
            #self._client.username_pw_set(username, password)
            self._client.on_connect = on_connect
            if(self.transport=="websockets"):
                self._client.tls_set()
            self._client.connect(self.broker, self.port)

            #Subscribe
            logging.info("Lets suscribe to topics!")
            self._subscribe(topic_to_subscribe)
            return True
            
        except Exception as e:
            logging.error(f"ERROR: In MQTT connection process: {e}")
            return False
        
    def set_callback(self, on_message_function):
        """Set callback for the client"""
        self._client.on_message = on_message_function

    def loop_forever(self):
        logging.info("START")
        self._client.loop_forever()

    def publish(self, topic, payload):
        logging.info("Send '" + payload + "' to '" + topic + "' topic . . .")
        self._client.publish(topic, payload)
        
    # Auxiliar
    def _subscribe(self, topics_to_subscribe):
        '''Subscribe to a single topic or a list of topics pass as parameter. If parameter is None, will subscribe to all config's topics'''
        if(topics_to_subscribe is not None):
            print("-> MQTTClient: Lets subscribe to: ",topics_to_subscribe)
            if(isinstance(topics_to_subscribe,list)):
                for topic in topics_to_subscribe:
                    self._client.subscribe(topic)
            else:
                self._client.subscribe(topics_to_subscribe)
        else:
            print("-> MQTTClient: Lets subscribe to config topics: ",self.topics)
            for topic in self.topics: 
                self._client.subscribe(topic)
    
    @staticmethod
    def create_from_config_file(json_config_file_path = config_file_path):
        f = open(json_config_file_path)
        config = json.load(f)
        return MqttClient(**config)

    @staticmethod
    def create_from_environment():
        broker = os.environ.get("MQTT_BROKER")
        port=int(os.environ.get("MQTT_PORT"))
        transport = os.environ.get("MQTT_TRANSPORT", "tcp")
        client_id=os.environ.get("MQTT_CLIENT_ID", "client_" + str(random.randint(0, 1000)))
        isAnonymous=os.environ.get("MQTT_AUTH", False)

        if None in (broker, port, client_id, isAnonymous):
            raise("No env variables!")
        
        topics=os.environ.get("MQTT_TOPICS").split(',')

        data = {
            "broker": broker,
            "port": port,
            "transport": transport,
            "client_id": client_id,
            "isAnonymous": isAnonymous,
            "credentials": {
                "username": os.environ.get("MQTT_USER"),
                "password": os.environ.get("MQTT_PASS"),
            },
            "topics": topics
        }
        logging.info("-----> LETS CREATE MQTT CLIENT")
        logging.info(data)
        return MqttClient(**data)

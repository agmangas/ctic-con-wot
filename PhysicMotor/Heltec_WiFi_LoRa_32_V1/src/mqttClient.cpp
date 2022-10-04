#include "mqttclient.h"

WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);

// Settings
const char *ssid = SECRET_WIFI_SSID;
const char *password = SECRET_WIFI_PASSWORD;

const char broker[] = "wss://wotmqtt.test.ctic.es";
int port = 443;
const char topic[] = "slides/command";

// Functions
void InitWifi()
{
    WiFi.begin(ssid, password);

    Serial.print("Connecting to WiFi...");
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nWifi is connected!");
}

void ConnectMQTT()
{
    Serial.print("Trying to connect to broker: ");
    Serial.print(broker);
    Serial.print(":");
    Serial.println(port);

    if (!mqttClient.connect(broker, port))
    {
        Serial.print("MQTT connection failed! Error code = ");
        Serial.println(mqttClient.connectError());

        while (1)
            ;
    }

    mqttClient.onMessage(onMQTTMessage);

    Serial.println("MQTT client connected to broker!");
    Serial.print("Subscribing to topic: ");
    Serial.print(topic);
    Serial.println("...");

    mqttClient.subscribe(topic);
    Serial.println("MQTT client subscribed to topic!");
}

void ReadMQTT()
{
    if (mqttClient.available())
    {
        Serial.print("--> New MQTT message in topic: ");
        Serial.println(topic);

        while (mqttClient.available())
            Serial.print((char)mqttClient.read());
    }
}

void onMQTTMessage(int messageSize)
{
    char msg[50];
    int i = 0;

    // we received a message, print out the topic and contents
    Serial.println("--> New MQTT message in topic: ");
    Serial.println(mqttClient.messageTopic());

    while (mqttClient.available())
    {
        Serial.print((char)mqttClient.read());
    }

    // use the Stream interface to print the contents
    while (mqttClient.available())
    {
        msg[i] = (char)mqttClient.read();
        i++;
    }
    Serial.print("The Message is: ");
    Serial.println(msg);

    Serial.println();
}
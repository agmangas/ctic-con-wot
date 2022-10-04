
#include <WiFi.h>
#include <ArduinoMqttClient.h>
#include "arduino_secrets.h"

void InitWifi();
void ConnectMQTT();
void ReadMQTT();
void onMQTTMessage(int);
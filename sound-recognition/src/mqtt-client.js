import mqtt from "mqtt/dist/mqtt";

const MQTT_URL = process.env.REACT_APP_MQTT_URL || "mqtt://localhost:9001";
const DIAPO_ID = 4;

const mqttClient = mqtt.connect(MQTT_URL);
const TOPIC_NEXT = "slides/command";

function connect() {
    mqttClient.on("connect", () => {
        console.log("MQTT CLIENT: Connected to MQTT broker", MQTT_URL);
    });
}

function disconnect() {
    mqttClient.end();
}

function next() {
    if (!mqttClient.connected) {
        console.log("MQTT CLIENT: Not connected to MQTT broker");
        return;
    }

    const infoToSend = {
        "method": "slide",
        "args": [DIAPO_ID]
    };
    console.log("MQTT CLIENT: Sending info:", infoToSend);
    mqttClient.publish(TOPIC_NEXT, JSON.stringify(infoToSend));

}

function liveEvent() {
    if (!mqttClient.connected) {
        console.log("MQTT CLIENT: Not connected to MQTT broker");
        return;
    }

    const infoToSend = {
        "method": "event",
        "args": [DIAPO_ID]
    };
    console.log("MQTT CLIENT: Sending info:", infoToSend);
    mqttClient.publish(TOPIC_NEXT, JSON.stringify(infoToSend));

}


export { connect, disconnect, next, liveEvent };
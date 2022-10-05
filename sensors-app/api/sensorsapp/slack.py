import json
import logging
import os

from flask import Blueprint, Response, request

from .mqtt_client.mqtt_client import MqttClient

BLUEPRINT_NAME = "slack"
blueprint = Blueprint(BLUEPRINT_NAME, __name__)

TOPIC = os.environ.get("MQTT_TOPICS", "slides/command")
SLIDE = os.environ.get("SLACK_BOT_SLIDE", 13)
EXPECTED_WORD = "siguiente"  # Hardcoded :)


@blueprint.route("", methods=["POST"])
def system():
    logging.info("Receive Slack POST")
    request_data = request.get_json()

    if "type" in request_data and request_data["type"] == "url_verification":
        logging.info("-->Challenge request, replying to confirm . . .")

        return {
            "challenge": request_data["challenge"],
        }
    elif "event" in request_data and request_data["event"]["type"] == "app_mention":
        logging.info("-->Incoming Slack message mentioning bot . . .")

        users = []
        messages = []
        blocks = request_data["event"]["blocks"]
        for block in blocks:
            elements = block["elements"]
            for element in elements:
                users.append(element["elements"][0]["user_id"])
                messages.append(element["elements"][1]["text"].lower())

        if any(EXPECTED_WORD in message for message in messages):
            logging.info("-->Message contains the Word, send to MQTT . . .")

            try:
                mqttClient = MqttClient.create_from_environment()
                logging.info("Connecting to MQTT broker: %s", mqttClient)
                mqttClient.connect()

                try:
                    msg_to_send = {"method": "slide", "args": [SLIDE]}
                    logging.info(msg_to_send)
                    mqttClient.publish(TOPIC, json.dumps(msg_to_send))
                    return Response(
                        "{'success':'True'}", status=200, mimetype="application/json"
                    )
                except Exception as e:
                    return Response(
                        f"{'success':'False', 'message': 'Error in MQTTClient: {e}'}",
                        status=500,
                        mimetype="application/json",
                    )
            finally:
                mqttClient.disconnect()

        return Response(
            "{'success':'False', 'message': 'Unexpected word'}",
            status=400,
            mimetype="application/json",
        )

    return Response(
        "{'success':'False', 'message': 'Unexpected event type'}",
        status=400,
        mimetype="application/json",
    )

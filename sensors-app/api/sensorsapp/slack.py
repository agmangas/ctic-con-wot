import datetime
import platform

from flask import Blueprint, request

BLUEPRINT_NAME = "slack"
blueprint = Blueprint(BLUEPRINT_NAME, __name__)


@blueprint.route("/", methods=['POST'])
def system():
    print("TESTESTES")
    request_data = request.get_json()
    print(request_data)
    return {
        "msg": "Siguiente diapositiva!",
        "challenge": request_data["challenge"],
    }

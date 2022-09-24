import datetime
import platform

from flask import Blueprint

BLUEPRINT_NAME = "info"
blueprint = Blueprint(BLUEPRINT_NAME, __name__)


@blueprint.route("/")
def system():
    return {
        "platform": platform.platform(),
        "utcnow": datetime.datetime.utcnow().isoformat(),
        "node": platform.node(),
        "python_version": platform.python_version(),
    }

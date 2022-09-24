import json
import logging
import os
import pprint
import traceback

import coloredlogs
from flask import Flask, current_app, jsonify
from flask_cors import CORS
from werkzeug.exceptions import HTTPException, NotFound

import sensorsapp.info

_STATIC_FOLDER = "appjs"
_STATIC_URL_PATH = ""
_DEFAULT_SECRET = "secret"
_ENV_LOG_LEVEL = "LOG_LEVEL"
_ENV_SECRET = "SECRET"
_PREFIX_INFO = "/api/info"

_logger = logging.getLogger(__name__)


def _init_logging():
    level = os.getenv(_ENV_LOG_LEVEL)
    level_default = level or "DEBUG"
    level_sql = level or "INFO"
    logging.getLogger("sqlalchemy.engine").setLevel(level_sql)
    coloredlogs.install(level=level_default)


def _config_from_env(app):
    secret_key = os.getenv(_ENV_SECRET, None)

    if not secret_key:
        _logger.warning("Undefined secret $%s: Using default", _ENV_SECRET)
        secret_key = _DEFAULT_SECRET

    conf = {
        "SECRET_KEY": secret_key,
    }

    _logger.info("Configuration:\n%s", pprint.pformat(conf))

    app.config.from_mapping(**conf)


def _jsonify_http_exception(err):
    response = err.get_response()

    response.data = json.dumps(
        {
            "code": err.code,
            "name": err.name,
            "description": err.description,
        }
    )

    response.content_type = "application/json"

    return response


def _handle_exception(err):
    if isinstance(err, NotFound):
        return current_app.send_static_file("index.html")

    if isinstance(err, HTTPException):
        return _jsonify_http_exception(err)

    _logger.warning("Request error\n%s", traceback.format_exc())

    code = 500
    data = {"code": code, "name": err.__class__.__name__, "description": str(err)}

    return jsonify(data), code


def _catch_all(path):
    return current_app.send_static_file("index.html")


def create_app(test_config=None):
    _init_logging()

    _logger.debug("Creating Flask app instance")

    app = Flask(
        __name__,
        instance_relative_config=True,
        static_folder=_STATIC_FOLDER,
        static_url_path=_STATIC_URL_PATH,
    )

    _config_from_env(app)

    if test_config is not None:
        _logger.debug("Test config:\n%s", pprint.pformat(test_config))
        app.config.from_mapping(test_config)
        _logger.debug("App config:\n%s", pprint.pformat(dict(app.config)))

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(sensorsapp.info.blueprint, url_prefix=_PREFIX_INFO)

    app.add_url_rule("/", view_func=_catch_all, defaults={"path": ""})
    app.add_url_rule("/<path:path>", view_func=_catch_all)

    app.register_error_handler(Exception, _handle_exception)

    CORS(app)

    return app

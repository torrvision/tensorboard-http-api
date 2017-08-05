# -*- coding: utf-8 -*-
import os
import requests
from flask import Blueprint, current_app, g, jsonify
# from .. import tbclient

main = Blueprint('main', __name__)


@main.before_request
def before():
    g.version = current_app.config['version']
    g.tensorboard_folder = current_app.config['tensorboard_folder']
    g.tensorboard_url = current_app.config['tensorboard_url']


@main.route("/", methods=['GET'], strict_slashes=False)
@main.route("/health", methods=['GET'], strict_slashes=False)
def health():
    response = requests.get(g.tensorboard_url + '/data/logdir')

    if response.status_code != 200:
        return "Tensorboard server not responding at {}".format(g.tensorboard_url)

    response = response.json()
    if response.get("logdir") != g.tensorboard_folder:
        message = "Tensorboard running in an incorrect folder ({}) instead of {}"\
            .format(response.get("logdir"), g.tensorboard_folder)
        return message, 400

    message = "Tensorboard running at '{}' in folder '{}'"\
        .format(g.tensorboard_url, g.tensorboard_folder)
    return jsonify({
        'health': 'OK',
        'version': g.version,
        'message': message,
        'tensorboard': {
            'logdir': g.tensorboard_folder,
            'address': g.tensorboard_url,
        }
    })

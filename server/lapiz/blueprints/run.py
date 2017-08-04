# -*- coding: utf-8 -*-
import os
import requests
from flask import Blueprint, current_app, g, jsonify, request
from .. import tbclient

run = Blueprint('run', __name__)


@run.before_request
def before():
    g.tensorboard_folder = current_app.config['tensorboard_folder']
    g.tensorboard_url = current_app.config['tensorboard_url']


@run.route("/data/runs", methods=['GET'], strict_slashes=False)
def get_all_runs():
    # folder_path = os.path.join(g.tensorboard_folder, runname)

    response = requests.get(g.tensorboard_url + '/data/runs')
    if response.status_code != 200:
        message = "Error while retrieving runs: {}".format(response.text)
        return message, 400
    runs_list = response.json()

    empty_runs_list = []
    # also collect empty folders, which correspond to created runs with no events yet
    for _, dirs, _ in os.walk(g.tensorboard_folder):
        for run_directory in dirs:
            if run_directory not in runs_list:
                empty_runs_list.append(run_directory)

    return jsonify({
        'runs': runs_list,
        'empty_runs': empty_runs_list,
    })


@run.route("/data/run/<runname>/summary", methods=['POST'], strict_slashes=False)
def post_run(runname):
    folder_path = os.path.join(g.tensorboard_folder, runname)
    payload = request.get_json()

    status = tbclient.write_summaries(runname, folder_path, payload)
    if status:
        return 'OK', 200
    return 'Error', 500

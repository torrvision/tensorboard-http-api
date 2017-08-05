# -*- coding: utf-8 -*-
import os
import io
import zipfile
from subprocess import Popen, PIPE
from flask import Blueprint, current_app, request, g
from flask import send_file
from .. import tbclient

backup = Blueprint('backup', __name__)


@backup.before_request
def before():
    g.tensorboard_folder = current_app.config['tensorboard_folder']


@backup.route("/data/backup/<runname>", methods=['GET'], strict_slashes=False)
def get_backup(runname):
    folder_path = os.path.join(g.tensorboard_folder, runname)

    # This method can be called outside the context of a run,
    # so the only existence test is the folder path.
    if not os.path.isdir(folder_path):
        message = "Non-existing run '{}'".format(runname)
        return message, 400

    # zip the directory structure under folder_path (/tmp/tensorboard/runname)
    # to a memory file
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(folder_path):
            for filepath in files:
                zf.write(os.path.join(root, filepath),
                         os.path.relpath(os.path.join(root, filepath),
                                         os.path.join(folder_path, '..')))

    memory_file.seek(0)
    return send_file(memory_file,
                     attachment_filename='{}.zip'.format(runname),
                     as_attachment=True)

    # return jsonify({
    #     'name': current_app.config['name'],
    #     'tmp': folder_path,
    #     'run': runname
    # })


@backup.route("/backup/<runname>", methods=['POST'], strict_slashes=False)
def post_backup(runname):
    folder_path = os.path.join(g.tensorboard_folder, runname)

    force = request.args.get('force')
    force = True if force.lower() == 'true' else False

    if runname in tbclient.tf_summary_writers and not force:
        message = "Run '{}' cannot be overwritten (force = False)"
        return message, 400

    # unzip without saving the zip
    # from io import BytesIO
    # from urllib.request import urlopen
    # from zipfile import ZipFile
    # zipurl = 'http://stash.compjour.org/data/1800ssa.zip'
    # with urlopen(zipurl) as zipresp:
    #     with ZipFile(BytesIO(zipresp.read())) as zfile:
    #         zfile.extractall('/tmp/mystuff4')

    # temporary zip file location before extraction
    zip_filepath = "/tmp/{}.zip".format(runname)

    if "archive" in request.files:
        backup_data = request.files["archive"]
        backup_data.save(zip_filepath)
    else:
        content_type = request.headers.get('Content-type', '')
        if (not content_type) or (content_type != "application/zip"):
            message = "Backup post request should contain a file or a zip"
            return message, 400
        with open(zip_filepath, "wb") as f:
            f.write(request.data)

    Popen("mkdir -p {}".format(folder_path), stdout=PIPE, shell=True)
    Popen("cd {}; unzip {}".format(folder_path, zip_filepath),
          stdout=PIPE, shell=True)

    os.remove(zip_filepath)

    tb_get_xp_writer(experiment)

    return "ok"

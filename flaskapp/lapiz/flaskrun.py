# -*- coding: utf-8 -*-
import optparse
import os
from . import __version__


def flaskrun(app, default_host="0.0.0.0", default_port="6007",
             default_tbfolder="/tmp"):
    """
    Takes a flask.Flask instance and runs it. Parses
    command-line flags to configure the app.
    """

    # Set up the command-line options
    parser = optparse.OptionParser()
    parser.add_option("-H", "--host",
                      help="Hostname of the Flask app " +
                      "[default %s]" % default_host,
                      default=default_host)
    parser.add_option("-P", "--port",
                      help="Port for the Flask app " +
                      "[default %s]" % default_port,
                      default=default_port)
    parser.add_option("--tensorboard-folder",
                      help="Tensorboard folder " +
                      "[default %s]" % default_tbfolder,
                      default=default_tbfolder)

    # Two options useful for debugging purposes, but
    # a bit dangerous so not exposed in the help message.
    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug",
                      help=optparse.SUPPRESS_HELP)

    options, _ = parser.parse_args()

    app.config.update({
        'name': 'romain',
        'tensorboard_folder': options.tensorboard_folder,
        'tensorboard_host': 'localhost',
        'tensorboard_port': 6006,
        'tensorboard_url': 'http://localhost:6006',
        'version': __version__
    })

    app.run(
        debug=options.debug,
        host=options.host,
        port=int(options.port),
    )

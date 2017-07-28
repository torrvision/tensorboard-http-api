# -*- coding: utf-8 -*-
from flask import Flask
from flaskrun import flaskrun
from blueprints.backup import backup

app = Flask(__name__)
app.register_blueprint(backup)

flaskrun(app)

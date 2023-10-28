#!/usr/bin/python3
""" define the index page of the api """
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """ check status of the api. """
    return jsonify({"status": "OK"})

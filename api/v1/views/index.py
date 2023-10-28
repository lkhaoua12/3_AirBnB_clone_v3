#!/usr/bin/python3
""" This module contains endpoint(route) status """

from api.v1.views import app_views
from flask import jsonify, request


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Returns api status """
    if request.method == 'GET':
        response_message = {
            "status": "OK"
        }
        return jsonify(response_message)

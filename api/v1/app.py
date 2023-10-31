#!/usr/bin/python3
""" This module define the app entrypoint """
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views, url_prefix='/api/v1')
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.teardown_appcontext
def teardown_db(obj):
    """ calls methods close() """
    storage.close()


@app.errorhandler(404)
def handle_errors(error):
    """ handle all routing errors. """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default=5000)
    app.run(host, int(port), threaded=True)

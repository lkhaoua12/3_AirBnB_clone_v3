#!/usr/bin/python3
""" define routes of the api """
import os
from flask import Flask
from models import storage
from api.v1.views import app_views

# app instance of Flask class.
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
# register app_views blueprint
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(Exception):
    storage.close()


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = os.getenv("HBNB_API_PORT", 5000)
    app.run(host=host, port=int(port), threaded=True)

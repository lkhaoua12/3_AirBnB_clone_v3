#!/usr/bin/python3
""" This module contains endpoint(route) status """

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/status', strict_slashes=False)
def status():
    """ Returns api status """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """ returns stats of each object """
    amenities_count = storage.count(Amenity)
    cities_count = storage.count(City)
    places_count = storage.count(Place)
    reviews_count = storage.count(Review)
    states_count = storage.count(State)
    users_count = storage.count(User)
    data = {"amenities": amenities_count,
            "cities": cities_count,
            "places": places_count,
            "reviews": reviews_count,
            "states": states_count,
            "users": users_count
            }
    return jsonify(data)

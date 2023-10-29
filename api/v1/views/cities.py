#!/usr/bin/python3
""" route for cities api endpoint. """
from api.v1.views import app_views
from flask import make_response, abort, request, jsonify
from models import storage
from models.city import City
from models.state import State


@app_views.route('states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_state_cities(state_id):
    """ return list of cities by state_id. """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """ return a city by it id """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ return a city by it id """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({})


@app_views.route('states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """ create a new city object. """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    body = request.get_json()
    if not body:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in body:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    body['state_id'] = state_id
    city = City(**body)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """ update a city object. """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    body = request.get_json()
    if not body:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in body.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200

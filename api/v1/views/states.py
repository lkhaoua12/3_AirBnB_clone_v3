#!/usr/bin/python3
""" create endpoint for states """
from models import storage
from flask import jsonify, abort, request
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """ get all states object in db """
    obj = []
    states = storage.all(State).values()
    for state in states:
        obj.append(state.to_dict())

    return jsonify(obj)


@app_views.route('/states/<id>', methods=['GET'], strict_slashes=False)
def get_state(id):
    """ get one state by it id """
    state = storage.get(State, id)
    if state:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ create a new state objects. """
    if not request.is_json:
        return jsonify({'error': 'Not a JSON'}), 400
    else:
        body = request.get_json()

    if 'name' not in body:
        return jsonify({'error': 'Missing name'}), 400
    else:
        state = State(**body)
        storage.save()
        return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ delete a State Object """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """ update state attr """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200

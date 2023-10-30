#!/usr/bin/python3
""" create endpoint for states """
from models import storage
from flask import jsonify, make_response, abort, request
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
        abort(400, 'Not a JSON')
    else:
        body = request.get_json()

    if 'name' not in body:
        abort(400, 'Missing name')
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
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """ update state attr """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    for key, value in state.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200

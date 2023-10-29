#!/usr/bin/python3
""" create endpoint for states """
from models import storage
from flask import jsonify, make_response, abort
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

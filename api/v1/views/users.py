#!/usr/bin/python3
""" endpoint view for users """

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def get_users():
    """get list of all users"""
    users = storage.all(User).values()
    users_json = [user.to_dict() for user in users]
    return jsonify(users_json)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """get a specified user by id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """deletes a user by id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return (jsonify({})), 200


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def post_user():
    """create a new user"""
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    if 'email' not in request.get_json():
        return jsonify({'error': 'Missing email'}), 400
    if 'password' not in request.get_json():
        return jsonify({'error': 'Missing password'}), 400
    body = request.get_json()
    user = User(**body)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """update a user by id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    for key, value in request.get_json().items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200

#!/usr/bin/python3
""" View object that handles RESTFul API actions for User"""


from flask import Flask, abort, request, jsonify
from models.user import User
from models import storage
from api.v1.views import app_views
from datetime import datetime


@app_views.route("/users",
                 methods=['GET'],
                 strict_slashes=False)
def get_all_user():
    """ Retrieve the list of all user objects"""
    user_objs = storage.all(User)
    return jsonify([user_obj.to_dict()
                    for user_obj in user_objs.values()])


@app_views.route("/users/<user_id>",
                 methods=['GET'],
                 strict_slashes=False)
def get_user_obj(user_id):
    """ retrieves a single user object"""
    user_obj = storage.get(User, user_id)
    if user_obj is None:
        abort(404)

    return jsonify(user_obj.to_dict())


@app_views.route("/users/<user_id>",
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Delete a user object"""
    user_obj = storage.get(User, user_id)
    if user_obj is None:
        abort(404)

    storage.delete(user_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/user",
                 methods=['POST'],
                 strict_slashes=False)
def create_user():
    """ create a user object """
    user_data = request.get_json()
    if user_data is None:
        abort(400, "Not a JSON")
    if "email" not in user_data:
        abort(400, "Missing email")
    if "password" not in user_data:
        abort(400, "Missing password")
    new_user = User(**user_data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>",
                 methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """ Update a user object """
    user_obj = storage.get(User, user_id)
    if user_obj is None:
        abort(404)
    user_data = request.get_json()
    if user_data is None:
        abort(400, "Not a JSON")
    ignored_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for key, value in user_data.items():
        if key not in ignored_keys:
            setattr(user_obj, key, value)
    setattr(user_obj, "updated_at", datetime.now())
    storage.save()
    return jsonify(user_obj.to_dict()), 200

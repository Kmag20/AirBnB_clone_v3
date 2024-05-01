#!/usr/bin/python3
""" Creates a view for City objects that handles all
default RESTFul API"""

from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage
from flask import jsonify, abort, request
from datetime import datetime


@app_views.route("/states/<state_id>/cities",
                 methods=['GET'], strict_slashes=False)
def city_states(state_id):
    """ List all city objects of a state """
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)

    cities = state_obj.cities
    return jsonify([city.to_dict() for city in cities])


@app_views.route("/cities/<city_id>",
                 methods=['GET'],
                 strict_slashes=False)
def get_or_delete_city(city_id):
    """  delete/retrieve a city object """
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)

    return jsonify(city_obj.to_dict())


@app_views.route("/cities/<city_id>",
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ Deletes a City object """
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)

    storage.delete(city_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("states/<state_id>/cities",
                 methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ create a new city object """
    city_data = request.get_json()
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    if not city_data:
        abort(400, "Not a JSON")
    if "name" not in city_data:
        abort(400, "Missing name")
    city_data.update({"state_id": state_obj.id})
    new_city = City(**city_data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>",
                 methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """ Updates a city object"""
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)

    city_data = request.get_json()
    if city_data is None:
        abort(400, "Not a JSON")

    for key, value in city_data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city_obj, key, value)
    setattr(city_obj, "updated_at", datetime.now())
    storage.save()
    return jsonify(city_obj.to_dict()), 200

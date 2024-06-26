#!/usr/bin/python3
""" A view for amenities """


from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from flask import abort, request, jsonify
from datetime import datetime


@app_views.route("/amenities",
                 methods=['GET'],
                 strict_slashes=False)
def get_all_amenities():
    """ Retrieve a list of all amenities"""
    amenity_objs = storage.all(Amenity)
    return jsonify([amenity.to_dict()
                    for amenity in amenity_objs.values()])


@app_views.route("/amenities/<amenity_id>",
                 methods=['GET'],
                 strict_slashes=False)
def get_amenity_obj(amenity_id):
    """ Retrieve a single amenity obj"""
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        abort(404)

    return jsonify(amenity_obj.to_dict())


@app_views.route("/amenities/<amenity_id>",
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ delete amenity object """
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        abort(404)

    storage.delete(amenity_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities",
                 methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """creates an amenity object"""
    amenity_data = request.get_json()
    if not amenity_data:
        abort(400, "Not a JSON")
    if "name" not in amenity_data:
        abort(400, "Missing name")
    new_amenity = Amenity(**amenity_data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>",
                 methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ Update an amenity object """
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        abort(404)
    amenity_data = request.get_json()
    if amenity_data is None:
        abort(400, "Not a JSON")
    for key, value in amenity_data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity_obj, key, value)
    setattr(amenity_obj, "updated_at", datetime.now())
    storage.save()
    return jsonify(amenity_obj.to_dict()), 200

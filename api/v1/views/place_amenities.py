#!/usr/bin/python3
""" defines the place amenities module"""


from flask import abort, jsonify
from models.place import Place
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """Get all amenities of a place"""
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)

    if storage.__class__.__name__ == 'DBStorage':
        return jsonify([amenity.to_dict()
                        for amenity in place_obj.amenities])

    return jsonify([amenity.to_dict()
                    for amenity in place_obj.amenity_ids])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """Delete an amenity from a place"""
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if storage.__class__.__name__ == 'DBStorage':
        if amenity not in place_obj.amenities:
            abort(404)
        place_obj.amenities.remove(amenity)
        storage.save()
    else:
        if amenity_id not in place_obj.amenity_ids:
            abort(404)
        place_obj.amenity_ids.remove(amenity_id)
        storage.save()

    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'],
                 strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """Link an amenity to a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if storage.__class__.__name__ == 'DBStorage':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
        storage.save()
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)
        storage.save()

    return jsonify(amenity.to_dict()), 201

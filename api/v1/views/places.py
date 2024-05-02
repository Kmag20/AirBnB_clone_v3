#!/usr/bin/python3
""" A view for amenities """


from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from flask import abort, request, jsonify
from datetime import datetime


@app_views.route("/cities/<city_id>/places",
                 methods=['GET'],
                 strict_slashes=False)
def get_all_places(city_id):
    """ Retrieve a list of all place"""
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    places_objs = city_obj.places
    return jsonify([places.to_dict()
                    for places in places_objs])


@app_views.route("/places/<place_id>",
                 methods=['GET'],
                 strict_slashes=False)
def get_place_obj(place_id):
    """ Retrieve a single place obj"""
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)

    return jsonify(place_obj.to_dict())


@app_views.route("/places/<place_id>",
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ delete place object """
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)

    storage.delete(place_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places",
                 methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """creates an place object"""
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    place_data = request.get_json()
    if not place_data:
        abort(400, "Not a JSON")
    if "user_id" not in place_data:
        abort(400, "Missing user_id")
    if "name" not in place_data:
        abort(400, "Missing name")
    user_obj = storage.get(User, place_data.user_id)
    if user_obj is None:
        abort(404)
    new_place = Place(**place_data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>",
                 methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """ Update an place object """
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)
    place_data = request.get_json()
    if place_data is None:
        abort(400, "Not a JSON")
    ignored_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]

    for key, value in place_data.items():
        if key not in ignored_keys:
            setattr(place_obj, key, value)
    setattr(place_obj, "updated_at", datetime.now())
    storage.save()
    return jsonify(place_obj.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Search for places based on JSON request body"""
    if not request.json:
        abort(400, "Not a JSON")

    states = request.json.get('states', [])
    cities = request.json.get('cities', [])
    amenities = request.json.get('amenities', [])

    if not states and not cities and not amenities:
        places = storage.all(Place).values()
    else:
        places = []
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                places.extend(state.places)

        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                places.extend(city.places)

    if amenities:
        filtered_places = []
        for place in places:
            place_amenities = {amenity.id for amenity in place.amenities}
            if set(amenities).issubset(place_amenities):
                filtered_places.append(place)
        places = filtered_places

    return jsonify([place.to_dict() for place in places])

#!/usr/bin/python3
""" A view for reviews """


from api.v1.views import app_views
from models.review import Review
from models.place import Place
from models.user import User
from models import storage
from flask import abort, request, jsonify
from datetime import datetime


@app_views.route("/places/<place_id>/reviews",
                 methods=['GET'],
                 strict_slashes=False)
def get_all_reviews(place_id):
    """ Retrieve a list of all reviews"""
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)

    review_objs = place_obj.reviews
    return jsonify([review.to_dict()
                    for review in review_objs.values()])


@app_views.route("/reviews/<review_id>",
                 methods=['GET'],
                 strict_slashes=False)
def get_review_obj(review_id):
    """ Retrieve a single review obj"""
    review_obj = storage.get(Review, review_id)
    if review_obj is None:
        abort(404)

    return jsonify(review_obj.to_dict())


@app_views.route("/reviews/<review_id>",
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ delete review object """
    review_obj = storage.get(Review, review_id)
    if review_obj is None:
        abort(404)

    storage.delete(review_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews",
                 methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """creates an review object"""
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)

    review_data = request.get_json()
    if not review_data:
        abort(400, "Not a JSON")
    if "text" not in review_data:
        abort(400, "Missing text")
    if "user_id" not in review_data:
        abort(400, "Missing user_id")
    user_obj = storage.get(User, review_data['user_id'])
    if user_obj is None:
        abort(404)
    new_review = Review(**review_data)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>",
                 methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """ Update an review object """
    review_obj = storage.get(Review, review_id)
    if review_obj is None:
        abort(404)
    review_data = request.get_json()
    if review_data is None:
        abort(400, "Not a JSON")
    for key, value in review_data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(review_obj, key, value)
    storage.save()
    return jsonify(review_obj.to_dict()), 200

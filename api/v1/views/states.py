#!/usr/bin/python3
"""
Flask route that returns json status response
"""

from api.v1.views import app_views
from models.state import State
from models import storage
from flask import jsonify, abort, request
from datetime import datetime



@app_views.route("/states",
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def all_states():
    """Retrieves the list of all State objects"""
    if request.method == 'POST':
        state_data = request.get_json()
        if not state_data:
            abort(400, "Not a JSON")
        elif "name" not in state_data:
            abort(400, "Missing name")
        new_state = State(**state_data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201
    elif request.method == 'GET':
        state_objs = storage.all(State).values()
        return jsonify([state.to_dict() for state in state_objs])


@app_views.route("/states/<state_id>", methods=['GET', 'PUT'])
def get_state(state_id):
    """Retrieves a single state object"""
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(state_obj.to_dict())
    elif request.method == 'PUT':
        state_data = request.get_json()

        for key, value in state_data.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(state_obj, key, value)
        setattr(state_obj, "updated_at", datetime.now())
        storage.save()
        return jsonify(state_obj.to_dict()), 200


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a state object"""
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    storage.delete(state_obj)
    storage.save()
    return jsonify({}), 200

#!/usr/bin/python3
""" app.py file"""

from flask import Flask, jsonify
from models import storage
from flask_cors import CORS
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)


"""Create the CORS instance to allow IPS"""
CORS(app, origins=['0.0.0.0'])


@app.teardown_appcontext
def teardown(exception):
    """ teardown """
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """ Error handler for 404 """
    return jsonify({"error": "Not found"}), 404


host_path = os.getenv('HBNB_API_HOST')
port_path = os.getenv('HBNB_API_PORT')


if __name__ == "__main__":
    host = '0.0.0.0' if host_path is None else host_path
    port = 5000 if port_path is None else port_path
    app.run(host=host, port=port, threaded=True)

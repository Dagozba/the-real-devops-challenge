from http import HTTPStatus
from os import environ

from flask import Flask, jsonify
from flask_pymongo import PyMongo

from src.mongoflask import MongoJSONEncoder, ObjectIdConverter, find_restaurants, find_restaurant

app = Flask(__name__)
app.config["MONGO_URI"] = environ.get("MONGO_URI")
app.json_encoder = MongoJSONEncoder
app.url_map.converters["objectid"] = ObjectIdConverter
mongo = PyMongo(app)


@app.route("/api/v1/restaurant")
def restaurants():
    restaurants_result = find_restaurants(mongo)
    return jsonify(restaurants_result)


@app.route("/api/v1/restaurant/<id>")
def restaurant(id):
    restaurant_result = find_restaurant(mongo, id)
    if not restaurant:
        return '', HTTPStatus.NO_CONTENT
    return jsonify(restaurant_result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=8080)

from datetime import date, datetime

import isodate as iso
from bson import ObjectId
from flask.json import JSONEncoder
from werkzeug.routing import BaseConverter


class MongoJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, (datetime, date)):
            return iso.datetime_isoformat(o)
        if isinstance(o, ObjectId):
            return str(o)
        else:
            return super().default(o)


class ObjectIdConverter(BaseConverter):
    def to_python(self, value):
        return ObjectId(value)

    def to_url(self, value):
        return str(value)


'''
I've created a new method in order to separate concerns and let each method do once thing and one thing well.
This way, the find restaurants can return a list and the find restaurant can return an object

This way, it's the services layer the one who decides which one to call depending on the http path,and not a condition
in code
'''


def find_restaurant(mongo, _id):
    return mongo.db.restaurant.find_one({"_id": ObjectId(_id)})


def find_restaurants(mongo):
    return list(mongo.db.restaurant.find({}))

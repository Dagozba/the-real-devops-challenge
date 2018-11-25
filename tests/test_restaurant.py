from unittest import TestCase

from bson.objectid import ObjectId
from mock import patch
import src.mongoflask

'''
I've reworked this test quite a bit. At first it was mocking the very same method that it was being tested, which led to fake results
as what was being asserted was exactly what the methods were being told to return.

I've also added tests for the service layer
'''


def mock_find_restaurant(query):
    data = [
        {"_id": ObjectId("55f14312c7447c3da7051b39"), "URL": "http://www.just-eat.co.uk/restaurants-1awok-pa7/menu",
         "address": "Unit 2 30 Greenock Road",
         "address line 2": "Bishopton", "name": "1A Wok", "outcode": "PA7", "postcode": "5JN", "rating": 5,
         "type_of_food": "Chinese"},
        {"_id": ObjectId("55f14312c7447c3da7051b38"),
         "URL": "http://www.just-eat.co.uk/restaurants-168chinese-ls18/menu", "address": "17 Alexandra Road",
         "address line 2": "West Yorkshire", "name": "168 Chinese & Cantonese Takeaway", "outcode": "LS18",
         "postcode": "4HE", "rating": 5.5, "type_of_food": "Chinese"},
        {"_id": ObjectId("55f14312c7447c3da7051b37"),
         "URL": "http://www.just-eat.co.uk/restaurants-1498thespiceaffair-pe11/menu", "address": "Red Lion Hotel",
         "rating": 5.5, "type_of_food": "Curry"}
    ]
    return next((restaurant for restaurant in data if restaurant.get('_id') == ObjectId(query.get("_id"))), [data])


class TestRestaurant(TestCase):

    @patch('flask_pymongo.PyMongo')
    def test_get_restaurants_returns_a_list_of_elements(self, mongo_mock):
        mongo_mock.db.restaurant.find = mock_find_restaurant
        data = src.mongoflask.find_restaurants(mongo_mock)
        self.assertEqual(list, type(data))

    @patch('flask_pymongo.PyMongo')
    def test_get_restaurant_returns_a_single_object_filtering(self, mongo_mock):
        mongo_mock.db.restaurant.find_one = mock_find_restaurant
        data = src.mongoflask.find_restaurant(mongo_mock, "55f14312c7447c3da7051b39")
        self.assertEqual(dict, type(data))
        self.assertTrue(data.get("type_of_food") == "Chinese")


class TestRestaurantAPI(TestCase):

    @patch('os.environ.get')
    def test_get_restaurants_flask_function_correct_response(self, environ_get):
        environ_get.return_value = 'mongodb://fake'
        from app import app as flask_app
        with flask_app.app_context():
            import app as service_app
            with patch('app.find_restaurants') as find_restaurants:
                find_restaurants.return_value = []
                r = service_app.restaurants()
                self.assertEqual(200, r.status_code)

    @patch('os.environ.get')
    def test_get_restaurant_flask_function_correct_response(self, environ_get):
        environ_get.return_value = 'mongodb://fake'
        from app import app as flask_app
        with flask_app.app_context():
            import app as service_app
            with patch('app.find_restaurant') as find_restaurant:
                find_restaurant.return_value = {}
                r = service_app.restaurant(1)
                self.assertEqual(200, r.status_code)

    @patch('os.environ.get')
    def test_get_restaurant_flask_function_empty_response_on_not_found_restaurant(self, environ_get):
        environ_get.return_value = 'mongodb://fake'
        from app import app as flask_app
        with flask_app.app_context():
            import app as service_app
            with patch('app.find_restaurant') as find_restaurant:
                find_restaurant.return_value = None
                r = service_app.restaurant(1)
                self.assertEqual(('', 204), r)
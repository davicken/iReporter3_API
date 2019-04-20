# File to handle tests for all red-flags endpoints
import unittest
from flask import request
import json
from api import app
from api.models.users_model import User, UsersData
from api.controllers.users_controller import my_users


class TestUserEndPoints(unittest.TestCase):
    # Class for testing the user endpoints
    def setUp(self):
        self.test_app = app.test_client(self)

 
    def tear_down(self):
        my_users.users_list.clear()

    # def test_get_all_users_when_usersList_not empty(self): 
    #     # tests for getting all red-flags  when the user list has 1 or more red-flag records
    #     input_data1 = {
    #         "email": "davicken@gmail.com",
    #         "first_name": "mwesigwa",
    #         "is_admin": true,
    #         "last_name": "david",
    #         "other_names": "keneth",
    #         "password": "pbkdf2:sha256:50000$xvf72qlX$2b313e4f5075f3488d2032df48f0a206f72d04c0063cadeb6188a6c39870064a",
    #         "phone_number": "0787550983",
    #         "registered_on": "2019-02-27 02:27",
    #         "user_id": "4f393f41-1f7b-49ba-80c1-052bdea874ff",
    #         "user_name": "davicken"
    #     }
    #     post_resp1 = self.test_app.post('/api/v1/users', content_type='application/json', data=json.dumps(input_data1), headers={'userId': 1})
    #     self.assertEqual(post_resp1.status_code,201)

    #     input_data2 = {
    #         "title": "embezzlement of funds",
    #         "images": ["image3", "image4"],
    #         "videos": ["video7", "video8"],
    #         "comment": "embezzlement is real evil",
        
    #            "location": {"lat": "0.3443", "long": "1.4334"}
    #     }
    #     post_resp2 = self.test_app.post('/api/v1/red-flags', content_type='application/json', data=json.dumps(input_data2), headers={'userId': 1})
    #     self.assertEqual(post_resp2.status_code,201)
    #     response = self.test_app.get('/api/v1/red-flags')
    #     self.assertEqual(response.status_code, 200)

    #     my_data = json.loads(response.data.decode())
    #     print(my_data['data'])
    #     self.assertEqual(len(my_data['data']), 2)
    #     self.assertEqual(my_data['data'][1]['title'], "embezzlement of funds")
    #     self.assertEqual(my_data['data'][1]['comment'], "embezzlement is real evil")
    #     self.assertEqual(my_data['data'][0]['images'], ["image1", "image2"])
    #     self.assertEqual(my_data ['data'][0]['location'], {"lat": "0.3333", "long": "1.0444"})
    #     self.assertEqual(my_data ['data'][0]['id'], 1)


    # def test_get_all_users_when_userlist_empty(self):
    #     # test the get all users endpoint when the users list has no red-flag records or empty
    #     my_users.users_list.clear()

    #     response = self.test_app.get('/api/v1/users')
    #     my_data = json.loads(response.data.decode())
    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(my_data['error'], 'There are no users records currently')
    #     self.assertIn('no users records', my_data['error'])


    
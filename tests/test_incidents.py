# File to handle tests for all incidents endpoints
import unittest
from flask import request
import json
from api import app
from api.models.incident_model import Incident, IncidentData
from api.controllers.incident_controller import my_incidents


class TestRedflagEndPoints(unittest.TestCase):
    # Class for testing the incident endpoints
    def setUp(self):
        self.test_app = app.test_client(self)

 
    def tear_down(self):
        my_incidents.incidents_list.clear()

       
    def test_index(self):
        # test for whether the default root url returns the correct message
        response = self.test_app.get('/api/v1/')
        self.assertEqual(response.status_code, 200)
        my_data = response.data.decode()
        message = {
            "message": [
                    "Welcome to Mwesigwa\'s iReporter APIs home",
                    "Incident Endpoints",
                    "#1 : GET /api/v1/incidents",
                    "#2 : GET /api/v1/incidents/<incident_id>",
                    "#3 : POST /api/v1/incidents",
                    "#4 : PATCH /api/v1/incidents/<incident_id>/location",
                    "#5 : PATCH /api/v1/incidents/<incident_id>/comment",
                    "#6 : DELETE /api/v1/incidents/<incident_id>"
                    ]
        }
        self.assertEqual(json.loads(my_data), message)

    def test_all_redflags_when_not_empty(self): 
        # tests for getting all incidents  when the incident list has 1 or more incident records
        input_data1 = {
            "title": "corruption at the office",
            "images": ["image1", "image2"],
            "videos": ["video1", "video2"],
            "comment": "corruption has become a menace",
            "location": {"lat": "0.3333", "long": "1.0444"}
        }
        post_resp1 = self.test_app.post('/api/v1/incidents', content_type='application/json', data=json.dumps(input_data1), headers={'userId': 1})
        self.assertEqual(post_resp1.status_code,201)

        input_data2 = {
            "title": "embezzlement of funds",
            "images": ["image3", "image4"],
            "videos": ["video7", "video8"],
            "comment": "embezzlement is real evil",
        
               "location": {"lat": "0.3443", "long": "1.4334"}
        }
        post_resp2 = self.test_app.post('/api/v1/incidents', content_type='application/json', data=json.dumps(input_data2), headers={'userId': 1})
        self.assertEqual(post_resp2.status_code,201)
        response = self.test_app.get('/api/v1/incidents')
        self.assertEqual(response.status_code, 200)

        my_data = json.loads(response.data.decode())
        print(my_data['data'])
        self.assertEqual(len(my_data['data']), 2)
        self.assertEqual(my_data['data'][1]['title'], "embezzlement of funds")
        self.assertEqual(my_data['data'][1]['comment'], "embezzlement is real evil")
        self.assertEqual(my_data['data'][0]['images'], ["image1", "image2"])
        self.assertEqual(my_data ['data'][0]['location'], {"lat": "0.3333", "long": "1.0444"})
        self.assertEqual(my_data ['data'][0]['id'], 1)


    def test_all_redflags_when_empty(self):
        # test the get all incident endpoint when the incident list has no incident records or empty
        response = self.test_app.get('/api/v1/incidents')
        my_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(my_data['error'], 'There are no incident records currently')
        self.assertIn('no incident records', my_data['error'])


    def test_create_redflag_with_correct_data(self):
        # test whether the status code and message after creating a redflag record are correct
        input_data = {
            "title": "corruption at the office",
            "images": ["image1", "image2"],
            "videos": ["video1", "video2"],
            "comment": "corruption has become a menace",
            "location": {"lat": "98854", "long": "888484"}
            }
        post_resp = self.test_app.post(
            '/api/v1/incidents', content_type='application/json', data=json.dumps(input_data), headers={'userId': 1})
        self.assertEqual(post_resp.status_code, 201)
        response = json.loads(post_resp.data.decode())
        my_data = response['data']
        self.assertEqual(response['status'], 201)
        self.assertEqual(my_data[0]['message'], "created incident record successfully")


    def test_create_redflag_with_wrong_comment_format(self):
        # tests a incident created with a wrong or totally no Comment 
        input_data1 = {
            # Comment with wrong data type
            "title": "corruption at the office",
            "images": ["image1", "image2"],
            "videos": ["video1", "video2"],
            "comment": 2,
            "location": {"lat": "98854", "long": "888484"}
            }
        input_data2 = {
            # No comment provided
            "title": "corruption at the office",
            "images": ["image1", "image2"],
            "videos": ["video1", "video2"],
            "comment": "",
            "location": {"lat": "98854", "long": "888484"}
            }
        input_data3 = {
            # comment with just white spaces
            "title": "corruption at the office",
            "images": ["image1", "image2"],
            "videos": ["video1", "video2"],
            "comment": "     ",
            "location": {"lat": "98854", "long": "888484"}
            }
        post_resp1 = self.test_app.post('/api/v1/incidents', content_type='application/json', data=json.dumps(input_data1), headers={'userId': 1})
        response = json.loads(post_resp1.data.decode())
        self.assertEqual(response['error'], 400)
        self.assertEqual(response['message'], "Comment and Title Should be strings")

        post_resp2 = self.test_app.post('/api/v1/incidents', content_type='application/json', data=json.dumps(input_data2), headers={'userId': 1})
        response = json.loads(post_resp2.data.decode())
        self.assertEqual(response['error'], 400)
        self.assertEqual(response['message'], "Comment and Title Should be strings")

        post_resp3 = self.test_app.post('/api/v1/incidents', content_type='application/json', data=json.dumps(input_data3), headers={'userId': 1})
        response = json.loads(post_resp3.data.decode())
        self.assertEqual(response['error'], 400)
        self.assertEqual(response['message'], "Comment and Title Should be strings")

    def test_create_redflag_with_wrong_location_format(self):
        # tests a incident created with a wrong location data type, length or totally no location 
        input_data1 = {
            # location with wrong data type
            "title": "corruption at the office",
            "images": ["image1", "image2"],
            "videos": ["video1", "video2"],
            "comment": " my comment",
            "location": "kalerwe"
            }
        input_data2 = {
            # No location provided
            "title": "corruption at the office",
            "images": ["image1", "image2"],
            "videos": ["video1", "video2"],
            "comment": "my comment",
            "location": {}
            }
        input_data3 = {
            # location with length of a dictionary greater than two
            "title": "corruption at the office",
            "images": ["image1", "image2"],
            "videos": ["video1", "video2"],
            "comment": "my comment",
            "location": {"lat": "98854", "long": "888484", "lat-long":"3454-2348"}
            }
        post_resp1 = self.test_app.post('/api/v1/incidents', content_type='application/json', data=json.dumps(input_data1), headers={'userId': 1})
        response = json.loads(post_resp1.data.decode())
        self.assertEqual(response['error'], 400)
        self.assertEqual(response['message'], "location should be a dictionary with two items; Latitude and Longitude coordinates")

        post_resp2 = self.test_app.post('/api/v1/incidents', content_type='application/json', data=json.dumps(input_data2), headers={'userId': 1})
        response = json.loads(post_resp2.data.decode())
        self.assertEqual(response['error'], 400)
        self.assertEqual(response['message'], "location should be a dictionary with two items; Latitude and Longitude coordinates")

        post_resp3 = self.test_app.post('/api/v1/incidents', content_type='application/json', data=json.dumps(input_data3), headers={'userId': 1})
        response = json.loads(post_resp3.data.decode())
        self.assertEqual(response['error'], 400)
        self.assertEqual(response['message'], "location should be a dictionary with two items; Latitude and Longitude coordinates")

    # def test_create_redflag_with_wrong_title_format(self):
    #     # tests a incident created with a wrong or totally no title 
    #     input_data1 = {
    #         # title with wrong data type
    #         "title": 34,
    #         "images": ["image1", "image2"],
    #         "videos": ["video1", "video2"],
    #         "comment": "my comment",
    #         "location": {"lat": "98854", "long": "888484"}
    #         }
    #     input_data2 = {
    #         # No title provided
    #         "title": "",
    #         "images": ["image1", "image2"],
    #         "videos": ["video1", "video2"],
    #         "comment": "my comment",
    #         "location": {"lat": "98854", "long": "888484"}
    #         }
    #     input_data3 = {
    #         # title with just white spaces
    #         "title": "    ",
    #         "images": ["image1", "image2"],
    #         "videos": ["video1", "video2"],
    #         "comment": "my comment",
    #         "location": {"lat": "98854", "long": "888484"}
    #         }
    #     post_resp1 = self.test_app.post('/api/v1/incidents', content_type='application/json', data=json.dumps(input_data1), headers={'userId': 1})
    #     response = json.loads(post_resp1.data.decode())
    #     self.assertEqual(response['error'], 400)
    #     self.assertEqual(response['message'], "Comment and Title Should be strings")

    #     post_resp2 = self.test_app.post('/api/v1/incidents', content_type='application/json', data=json.dumps(input_data2), headers={'userId': 1})
    #     response = json.loads(post_resp2.data.decode())
    #     self.assertEqual(response['error'], 400)
    #     self.assertEqual(response['message'], "Comment and Title Should be strings")

    #     post_resp3 = self.test_app.post('/api/v1/incidents', content_type='application/json', data=json.dumps(input_data3), headers={'userId': 1})
    #     response = json.loads(post_resp3.data.decode())
    #     self.assertEqual(response['error'], 400)
    #     self.assertEqual(response['message'], "Comment and Title Should be strings")

    
    # def test_edit_location_with_correct_id(self):
    #     # create an admin user since there's no option for signing him up
    #     incident = Incident(
    #         incident_id = 1,
    #         location = {
    #             "lat": "0.0460",
    #             "long": "0.5557"
    #         },
    #         created_by = "1",
    #         title = "corruption3",
    #         comment = "my comment",
    #         images =  [
    #             "image1",
    #             "image2"
    #         ],
    #         videos = [
    #             "video1",
    #             "video2"
    #         ], 
    #         createdOn = "2019-03-18 03:31",
    #         inc_type = "incident", 
    #         status= "draft"
    #     )
    #     my_incidents.incidents_list.append(incident)

    #     input_data = {
    #         "title": "corruption3",
    #         "images": ["image1", "image2"],
    #         "videos": ["video1", "video2"],
    #         "comment": "corruption has become a menace",
    #         "location": {"lat": "0.0460", "long": "0.5557"}
    #         }
    #     patch_resp = self.test_app.post(
    #         '/incidents/1/location', content_type='application/json', data=json.dumps(input_data), headers={'userId': 1})
       
    #     response = json.loads(patch_resp.data.decode())
    #     my_data = response['data']
    #     self.assertEqual(response['status'], 202)
    #     self.assertIn('updated to', my_data['message'])




   
from flask import request, jsonify
from api.helpers.validation import validate_create_redflag_data
from api.models.database import DatabaseConnect
from datetime import datetime
current_time = datetime.now().strftime("%Y-%m-%d %H:%M")

# my_incidents = IncidentData()

db = DatabaseConnect()

class IncidentController:

    def index(self):
        # welcome message
        return jsonify(
            {
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
            })
            

    def create_incidents(self):
        # create a incident using request data
        data = request.get_json()
        title = data.get('title')
        incident_type = data.get('type')
        location = data.get('location')
        comment = data.get('comment')
        images = data.get('images')
        videos = data.get('videos')
        created_by = request.headers["userId"]
        status = "draft"
        created_on = current_time
    
        # validate the input data
        if validate_create_redflag_data(data):
            return jsonify({"error": 400,
                            "message": validate_create_redflag_data(data)
                            }), 400

        incident_id = db.create_incident(incident_type, location, status, title, images, videos, created_by, comment, created_on)

        return jsonify({'status': 201, 'data': [{
            "id": incident_id,
            "message": "created incident record successfully" 
            }]
            }),201

    # def get_all_incidents(self):
    #     # get all existing incidents
    #     json_incidents = []
    #     for redflag in my_incidents.incidents_list:
    #         json_incidents.append(redflag.to_json())

    #     if len(json_incidents) < 1:
    #         return jsonify({
    #             'error': 'There are no incident records currently',
    #             'status': 404
    #             }), 404

    #     return jsonify({
    #         'status': 200, 
    #         'data': json_incidents
    #         })


    # def get_incidents(self, incident_id):
    #     # get a specific incident based on its id
    #     for redflag in my_incidents.incidents_list:
    #         if redflag.__dict__['incidentId'] == incident_id:
    #             return jsonify({
    #                 'status': 302,
    #                 'data': [redflag.to_json()]
    #             }), 302

    #     return jsonify({
    #         'status': 204,
    #         'error': 'That incident record does not exist'
    #     }), 200

    # def delete_record(self, incident_id):
    #     # delete a single incident record by its id
    #     for redflag in my_incidents.incidents_list:
    #         if redflag.__dict__['incidentId'] == incident_id:
    #             my_incidents.incidents_list.remove(redflag)
    #             return jsonify({
    #                 'status': 200,
    #                 'data': [{
    #                     'id': redflag.__dict__['incidentId'],
    #                     'message': 'incident record with id {} has been deleted successfully'.format(redflag.__dict__['incidentId'])
    #                 }]
    #             }), 200

    #     return jsonify({
    #         'status': 204,
    #         'error': 'That incident record does not exist'
    #     }), 404

    # def edit_location_and_comment(self, incident_id):
    #     # edit specific incident record location
    #     if not request.json:
    #         return jsonify({
    #             'status': 400,
    #             'error': 'There is no request data given, Provide new data'
    #         }), 400
    #     if 'location' in request.get_json():
    #         new_location = request.get_json()
    #         if 'location' not in new_location:
    #             return jsonify({
    #                 "status": 400,
    #                 "error": "wrong location format. follow this example ->> 'location':{'lat': '0.55767630', 'long': '0.355475685'}"
    #             }), 417
    #         for redflag in my_incidents.incidents_list:
    #             if redflag.__dict__["incidentId"] == incident_id:
    #                 redflag.__dict__["location"] = new_location["location"]
    #                 return jsonify({
    #                     "status": 202,
    #                     "data": [{
    #                         "message": "Location of incident record id {} updated to {}".format(incident_id, new_location["location"])
    #                     }]
    #                 }), 202

    #     elif 'comment' in request.get_json():
    #         new_comment = request.get_json()        
    #         if 'comment' not in new_comment:
    #             return jsonify({
    #                 "status": 400,
    #                 "error": "wrong comment format. follow this example ->> 'comment':'My incident comment'"
    #             }), 417
                
    #         for redflag in my_incidents.incidents_list:
    #             if redflag.__dict__["incidentId"] == incident_id:
    #                 redflag.__dict__["comment"] = new_comment["comment"]
    #                 return jsonify({
    #                     "status": 202,
    #                     "data": [{
    #                         "message": "comment of incident record id {} updated to {}".format(incident_id, new_comment["comment"])
    #                     }]
    #                 }), 202

    #     return jsonify({
    #         "status": 404,
    #         "error": "Sorry, that incident record does\'t exist"
    #     }), 404

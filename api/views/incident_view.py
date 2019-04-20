from flask import request, jsonify, Blueprint
from api import app
from api.controllers.incident_controller import IncidentController

b_print = Blueprint("incident_view", __name__, url_prefix="/api/v1")
incident_obj = IncidentController()

# A landing Page welcome message endpoint
@b_print.route('/', methods=['GET'])
def home_welcome_message():
    return incident_obj.index()

# create a red-flag end-point
@b_print.route('/incidents', methods=['POST'])
def create_new_incidents():
    return incident_obj.create_incidents()

# get all red-flags end-point
@b_print.route('/incidents', methods=['GET'])
def get_all_created_incidents():
    return incident_obj.get_all_incidents()

# get a single red-flag by its id endpoint
@b_print.route('/incidents/<int:incident_id>', methods=['GET'])
def get_specific_incident(incident_id):
    return incident_obj.get_incidents(incident_id)

# delete a single red-flag record by its id endpiont
@b_print.route('/incidents/<int:incident_id>', methods=['DELETE'])
def delete_specific_record(incident_id):
    return incident_obj.delete_record(incident_id)

# edit specific red-flag record location endpoint
@b_print.route('/incidents/<int:incident_id>/location', methods=['PATCH'])
def edit_specific_location(incident_id):
    return incident_obj.edit_location_and_comment(incident_id)

# edit specific red-flag record  comment endpoint
@b_print.route('/incidents/<int:incident_id>/comment', methods=['PATCH'])
def edit_specific_comment(incident_id):
    return incident_obj.edit_location_and_comment(incident_id)
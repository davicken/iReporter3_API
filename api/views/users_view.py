from functools import wraps

from flask import Blueprint, jsonify, request

import jwt
from api import app
from api.controllers.users_controller import UsersController, my_users

app.config['SECRET_KEY']= 'thisismysecretkey'

ub_print = Blueprint("users_view", __name__, url_prefix="/api/v1/users")
user_obj = UsersController()

# # A landing Page welcome message endpoint
# @route('/', methods=['GET'])
# def home_welcome_message():
#     return user_obj.index()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message':'token is missing',
                'error':401  
            }),401
        try:
            tkn_data = jwt.decode(token, app.config['SECRET_KEY']) # eg. {'user_id': 'b6fc9388-ebdf-4353-a5ee-3dc584df8d79', 'exp': 1553521558}
            # get a specific user based on his id
            if len (my_users.users_list) < 1:
                return jsonify({
                    'error': 'There are no users records currently',
                    'status': 404
                    }), 404

            for user in my_users.users_list:
                if user.__dict__['userId'] == tkn_data['user_id']:
                    current_user = user
        except:
            return jsonify({'message':'token is invalid or expired. You should login again.',
                'error':401
            }),401
        return f(current_user, *args, **kwargs)
    return decorated

# create a new user end-point
@ub_print.route('', methods=['POST'])
def register_new_user():
    return user_obj.create_user()

# get all users end-point
@ub_print.route('', methods=['GET'])
@token_required
def get_all_created_users(current_user):
    # if is_admin is False
    if not current_user.__dict__["isAdmin"]: #same as: current_user.__dict__["isAdmin"] == False
        return jsonify({'message': 'can not perform this action. You need to login as an admin!'})
    return user_obj.get_all_users()

# get a single user by his id endpoint
@ub_print.route('/<user_id>', methods=['GET'])
@token_required
def get_specific_redflag(current_user, user_id):
    # if is_admin is False/ not admin
    if not current_user.__dict__["isAdmin"]: #same as: current_user.__dict__["isAdmin"] == False
        return jsonify({'message': 'can not perform this action. You need to login as an admin!'})
    return user_obj.get_user(user_id)

# delete a single user record by its id endpiont
@ub_print.route('/<user_id>', methods=['DELETE'])
@token_required
def delete_specific_user_record (current_user, user_id):
    return user_obj.delete_user(user_id)

# edit specific user record  endpoint
@ub_print.route('/<user_id>', methods=['PATCH'])
@token_required
def edit_specific_user_info(current_user, user_id):
    return user_obj.edit_user(user_id)

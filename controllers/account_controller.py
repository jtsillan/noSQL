from passlib.hash import pbkdf2_sha256 as sha256
from flask import jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt
from errors.not_found import NotFound
from errors.validation_error import ValidationError
from models import User
from validators.account import check_profile_picture_max_size, validate_account, validate_update_profile_picture

# /api/account/password
@jwt_required()
def account_password_route_handler():
    user_id = get_jwt()['sub']
    request_body = request.get_json()
    if request_body:
        if 'password' in request_body:            
            account = User.get_by_id(user_id)
            account.password = sha256.hash(request_body['password'])
            account.update()
            return jsonify(account = account.to_json())
        raise ValidationError(message='password is required')
    raise ValidationError(message='request body is required')


# /api/account/profile_picture
""" @jwt_required()
@validate_update_profile_picture()
@check_profile_picture_max_size(max_size_in_kt=200)
def account_profile_picture_route_handler():
    request_body = request.get_json()
    user_id = get_jwt()['sub']
    account = User.get_by_id(user_id)
    account.profile_picture = request_body['profile_picture']
    # kutsutaan päivityksen jälkeen update-metodia
    account.update()
    # palautetaan päivitetty user account jsonifylla
    return jsonify(account = account.to_json()) """
    

# /api/account
class AccountRouteHandler(MethodView):
    @jwt_required()
    def get(self):
        user_id = get_jwt()['sub']
        account = User.get_by_id(user_id)
        return jsonify(account=account.to_json())

    @jwt_required()
    @validate_account
    def patch(self):
        # otetaan request_body vastaan
        request_body = request.get_json()
        # haetaan käyttäjä jwt:n subilla
        user_id = get_jwt()['sub']
        account = User.get_by_id(user_id)
        # päivitetään löydetyn käyttäjän (account) username, sillä joka on reqeust_bodyssä
        account.username = request_body['username']
        # kutsutaan päivityksen jälkeen update-metodia
        account.update()
        # palautetaan päivitetty user account jsonifylla
        return jsonify(account = account.to_json())
        


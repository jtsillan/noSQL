
from flask import request
from errors.validation_error import ValidationError


def validate_account(func):
    def validate_account_wrapper(*args, **kwargs):
        request_body = request.get_json()
        if request.method:
            if 'username' in request_body:
                return func(*args, **kwargs)
            else:
                raise ValidationError(message='username is required')
        else:
            raise ValidationError(message='request body required')
    return validate_account_wrapper


def validate_update_profile_picture(func):
    def validate_update_profile_picture_wrapper(*args, **kwargs):
        request_body = request.get_json()
        if request.method:
            if 'profile_picture' in request_body:
                return func(*args, **kwargs)
            else:
                raise ValidationError(message='profile picture is required')
        else:
            raise ValidationError(message='request body is required')
    return validate_update_profile_picture_wrapper


def check_profile_picture_max_size(max_size_in_kt=200):
    pass
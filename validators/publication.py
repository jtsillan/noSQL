from flask import request
from flask_jwt_extended import get_jwt

from errors.unauthorized import Unauthorized
from errors.validation_error import ValidationError


def validate_publication_route_handler(publication_route_handler):
    def validate_update_publication_wrapper(*args, **kwargs):
        logged_in_user = get_jwt()
        request_body = request.get_json()
        if request.method == 'GET':
            return publication_route_handler(*args, **kwargs)
        elif request.method == 'PATCH':            
            if not logged_in_user:
                raise Unauthorized()    
                
            if not request_body:
                raise ValidationError('request body is required')
            if 'title' not in request_body:
                raise ValidationError('title is required')
            if 'description' not in request_body:
                raise ValidationError('description is required')
            if 'visibility' not in request_body:
                raise ValidationError('visibility is required')
            return publication_route_handler(*args, **kwargs)
        elif request.method == 'DELETE':                       
            #logged_in_user = get_jwt()
            #request_body = request.get_json()            
            if not logged_in_user:
                raise Unauthorized()
            return publication_route_handler(*args, **kwargs)
            # kirjoita tähän koodi, jolla tarkistat, että käyttäjä on kirjautunut sisään (vihje: katso ylempi ehtolause)
        else:
            return publication_route_handler(*args, **kwargs)

    return validate_update_publication_wrapper


def validate_comments_route_handler(comments_route_handler):
    def validate_comments_route_handler_wrapper(*args, **kwargs):
        if request.method == 'GET':
            return comments_route_handler(*args, **kwargs)
        elif request.method == 'POST':
            request_body = request.get_json()
            if not request_body:
                raise ValidationError('request body is required')
            if 'comments' not in request_body:
                raise ValidationError('comment is required')
            return comments_route_handler(*args, **kwargs)
        
    return validate_comments_route_handler_wrapper
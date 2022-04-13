
from flask import jsonify, request
from models import Publication


def publications_route_handler():
    if request.method == 'GET':
        publications = Publication.get_all()
        publications_in_json_format = Publication.list_to_json(publications)
        return jsonify(publications=publications_in_json_format)

    elif request.method == 'POST':
        request_body = request.get_json()
        title = request_body['title']
        description = request_body['description']
        url = request_body['url']
        new_publication = Publication(title, description, url)
        new_publication.create()
        return jsonify(publication=new_publication.to_json())


def publication_route_handler(_id):
    pass


def publication_comment_route_handler(_id):
    pass
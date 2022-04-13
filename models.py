
import pymongo
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
from passlib.hash import pbkdf2_sha256 as sha256
from config import Config

from errors.not_found import NotFound

# käytä tätä jos on paikallinen mongodb-palvelin
# mongodb://localhost:27017/

client = pymongo.MongoClient(Config.CONNECT_STR, server_api=ServerApi('1'))
db = client.noSQL

# jokaiselle MongoDB:n collectionille / esim. MySGL tablelle
# tehdään luokka (tämä luokka on ns. model-luokka)
# jokainen model-luokka sisältää samat tiedot, kuin tietokannan
# collection / table (esim. username)

# model-luokkaan kuuluu CRUD:n toiminnallisuudet, joista jokainen
# on model-luokan funktio / metodi

# CRUD
# C => create()
# R => get_all() ja get_by_id()
# U => update()
# D => delete()

# mitä hyötyä modellista sitten on,
# jos CRUD:n voi tehdä suoraan controlleriinkin?

# koska Separation of Concerns
# käytännössä SoC tarkoittaa tässä sitä, että
# controllerin tehtävä on huolehtia route_handlereista
# eikä tietokantahauista

class Publication:
    def __init__(self, title, description, url, owner=None, likes=[], shares=0, share_link=None, comments=[], visibility=2, _id=None):
        # 2: kaikille julkinen, 1: näkyy vain kirjautuneille, 0: näkyy vain julkaisun omistajille + admin
    
        self.title = title
        self.description = description
        self.url = url
        self.owner = owner
        self.likes = likes
        self.shares = shares
        self.share_link = share_link
        self.comments = comments
        self.visibility = visibility
        if _id is not None:
            # jotta jsonify ei epäonnistu, _id pitää muuttaa str-funktiolla
            # merkkijonoksi
            _id = str(_id)
        self._id = _id

    
    @staticmethod
    def list_to_json(publications_list): # [models.Publication, ...]
        publications_in_json_format = []
        for publication_object in publications_list: # publication_object = models.Publication
            publication_object_in_json_format = publication_object.to_json() # {'title': 'eka'}
            # [{'title': 'eka', ...}]
            publications_in_json_format.append(publication_object_in_json_format)

        return publications_in_json_format


    @staticmethod
    # on tavanmukaista, että model-luokan @staticmethod, jolla HAETAAN tietoa
    # palauttavat ko. luokan tyyppisiä muuttujia (tässä tilanteessa 'dictonary')
    def get_all():
        publications = []
        publications_cursor = db.publications.find()
        for publication in publications_cursor:
            title = publication['title']
            description = publication['description']
            url = publication['url']
            _id = publication['_id']
           
            publication_object = Publication(title, description, url, _id=_id)
            publications.append(publication_object)
        return publications



    def create(self):
        result = db.publications.insert_one({
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'owner': self.owner,
            'likes': self.likes,
            'shares': self.shares,
            'share_link': self.share_link,
            'comments': self.comments,
            'visibility': self.visibility         
        })
       
        self._id = str(result.inserted_id)
        

    def to_json(self):
        publication_in_json_format = {
            '_id': str(self._id),
            'title': self.title,
            'description': self.description
        }
        return publication_in_json_format



class User:
    def __init__(self, username, password=None, role='user', _id=None):
        self.username = username
        self.password = password
        self.role = role

        if _id is not None:
            _id = str(_id)
        self._id = _id

    
    @staticmethod
    def get_by_username(username):
        user = db.users.find_one({'username': username})
        if user is None:
            raise NotFound(message='User not found')
        return User(username, 
        password=user['password'], 
        role=user['role'],
        _id=user['_id'])

    # kun classin funktio / metodi ei ole @staticmethod
    # sen ensimmäinen argumentti on self
    # selfin kautta pääsee kaikkiin luokan muuttujiin käsiksi
    # self.username
    def create(self):       
        result = db.users.insert_one({'username': self.username, 
        'password': sha256.hash(self.password), 'role': self.role})
        self._id = str(result.inserted_id)

    # sama kuin yllä, mutta @staticmethodilla voi käyttää jompaa kumpaa
    # tässä tilanteessa helpompaa käyttää yllä olevaa, koska on helpompaa
    # lisätä parametreja 

    #@staticmethod
    #def create_user(username):
    #    result = db.users.insert_one({'username': username})
    #    return User(username, _id=result.inserted_id)

    # CRUD:n U
    def update(self):
        db.users.update_one(
            {'_id': ObjectId(self._id)},
            {'$set': {'username': self.username}}
        )


    # CRUD:n R (kaikki käyttäjät)
    @staticmethod
    def get_all():
        users = []
        users_cursor = db.users.find()
        for user in users_cursor:
            users.append(User(user['username'], _id=str(user['_id'])))
        return users


    # CRUD:n D (staattisella metodilla) -> user_route_handler 'DELETE' (kommenteissa)
    @staticmethod
    def delete_by_id(_id):
        db.users.delete_one({'_id': ObjectId(_id)})


    # CRUD:n R (yksi käyttäjä _id:n perusteella)
    @staticmethod
    def get_by_id(_id):
        user = db.users.find_one({'_id': ObjectId(_id)})
        return User(user['username'], _id=str(user['_id']))


    # CRUD:n D (Delete, eli yksittäisen käyttäjän poisto)
    def delete(self):
        db.users.delete_one({'_id': ObjectId(self._id)})


    @staticmethod
    def list_to_json(user_list):
        json_list = []
        for user in user_list:
            user_in_json_format = user.to_json()
            json_list.append(user_in_json_format)
        return json_list


    def to_json(self):
        user_in_json_format = {
            '_id': str(self._id),
            'username': self.username,
            'role': self.role
        }
        return user_in_json_format
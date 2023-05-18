from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_basicauth import BasicAuth
from flask_marshmallow import Marshmallow

api = Api()
db = SQLAlchemy()
basic_auth = BasicAuth()
ma = Marshmallow()
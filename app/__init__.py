from flask import Flask

from .extensions import api, db, basic_auth, ma
from .resources.posts_resources import posts_ns
from .resources.comments_resources import comments_ns

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config.from_pyfile('config.py')

    api.init_app(app)
    db.init_app(app)
    ma.init_app(app)

    basic_auth.init_app(app)
    app.app_context().push()
    db.create_all()

    api.add_namespace(posts_ns)
    api.add_namespace(comments_ns)

    return app
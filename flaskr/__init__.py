import os
from flask_migrate import Migrate
from flask import Flask
from .extensions import db, login_manager
from .models import User

def create_app(config_file='config.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)

    migrate = Migrate(app,db)

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    from .db import create_tables
    app.cli.add_command(create_tables)

    return app

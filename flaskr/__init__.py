import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='df62557026976cf4afd91d17dffe277b22385b89d40900468e4f440e46d26e42',
        DATABASE_URL=os.path.join(app.instance_path, 'postgres://bxbrsvzalhluop:a983f9e5ccd65456c515adaeda2d44f437c427508b5339709cedcf4ce3abf267@ec2-54-236-156-167.compute-1.amazonaws.com:5432/db0j4u8u8tarbl'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app

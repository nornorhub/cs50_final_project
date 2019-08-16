# Imports
import os


from flask import Flask
from . import db, auth, index


# Creates the app and sets all required variables
def create_app(test_config=None):

    # The flask app
    app = Flask(__name__, instance_relative_config=True)

    # Sets the app configuration 
    # (This secret key is just for development purposes)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )

    # Sets the testing config
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    # Creates the instance folder
    try:
        os.mkdir(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    # Registers view blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(index.bp)

    return app
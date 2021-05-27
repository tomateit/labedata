"""
App initialization prep.
create_app() Sets up blueprints and configs. returns configured flask app
"""
import os
from flask import Flask, session, g
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()
from .models.user import User

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    print("Flask will be configured as", __name__)
    # app.config.from_object(os.environ.get('FLASK_ENV') or 'config.DevelopementConfig')

    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY"),
        DATABASE=Path(app.instance_path, 'labedata.sqlite'),
        INPUT_DIR=Path(__file__, "..", "..", "input").resolve(),
        OUTPUT_DIR=Path(__file__, "..", "..", "output").resolve()
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
        app.config["INPUT_DIR"].mkdir(parents=True, exist_ok=True)
        app.config["OUTPUT_DIR"].mkdir(parents=True, exist_ok=True)
    except OSError:
        print(f"Could not create {app.instance_path}")

    from . import db
    db.init_app(app)

    from . import index
    app.register_blueprint(index.bp)
    app.add_url_rule('/', endpoint='index')

    from . import auth
    app.register_blueprint(auth.bp)

    from . import dataset
    app.register_blueprint(dataset.bp)

    @app.before_request
    def load_logged_in_user():
        user_id = session.get("user_id")
        if user_id is None:
            g.user = None
        else:
            g.user = User.fetch_by_user_id(user_id)

    return app

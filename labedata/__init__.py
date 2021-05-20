import os
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, session, g
from pathlib import Path
from .models.user import User

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    print("Flask will be configured as", __name__)
    # app.config.from_object(os.environ.get('FLASK_ENV') or 'config.DevelopementConfig')

    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY"),
        DATABASE=Path(app.instance_path, 'labedata.sqlite'),
        PORT=os.environ.get("PORT", 5567),
        IP=os.environ.get("IP"), 
        #TODO get in and out dirs from env
        INPUT_DIR=Path(__file__,"..","..", "input").resolve(),
        OUTPUT_DIR=Path(__file__,"..","..","output").resolve()
    )

    # if test_config is None:
    #     # load the instance config, if it exists, when not testing
    #     app.config.from_pyfile('config.py', silent=True)
    # else:
    #     # load the test config if passed in
    #     app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
        app.config["INPUT_DIR"].mkdir(parents=True, exist_ok=True)
        app.config["OUTPUT_DIR"].mkdir(parents=True, exist_ok=True)
    except OSError:
        print(f"Could not create {app.instance_path}")
        pass

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
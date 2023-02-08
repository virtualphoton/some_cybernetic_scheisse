import os
from pathlib import Path

from dotenv import dotenv_values
from flask import Flask
from flask_cors import CORS

from .extensions import db
from .routes import db_api, auth

env_vars = dotenv_values(Path(__file__).parent / ".env" )
BACKEND_URL = env_vars["BACKEND_URL"]
DB_PATH = env_vars["DB_PATH"]
SECRET_KEY = env_vars["SECRET_KEY"]

def create_app():
    app = Flask(__name__)
    
    # bypass http
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    app.config["Access-Control-Allow-Origin"] = "*"
    app.config["Access-Control-Allow-Headers"]="Content-Type"
    app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DB_PATH}'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = SECRET_KEY

    CORS(app)
    db.init_app(app)
    
    app.register_blueprint(db_api)
    app.register_blueprint(auth)
    
    return app


def create_db():
    app = create_app()
    with app.app_context():
        db.create_all()
        db.session.commit()

from .oauth_tools import register_google
from flask import Blueprint, session, redirect
from authlib.integrations.flask_client import OAuth
from flask import url_for, current_app, render_template
from flask_jwt_router import JwtRoutes
from flask_sqlalchemy import SQLAlchemy
from flask import request

db = SQLAlchemy()

authorization = Blueprint('authorization', __name__)

current_app.config["JWT_ROUTER_API_NAME"] = "/api/v1"


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


jwt_routes = JwtRoutes()
jwt_routes.init_app(
    current_app,
    entity_models=[UserModel],
)


@authorization.route("/api/v1/register", methods=["POST"])
def register():
    return "I don't need authorizing!"


@authorization.route("/login", methods=["POST"])
def login():
    data = jwt_routes.google.oauth_login(request)  # Pass in Flask's request
    return data, 200

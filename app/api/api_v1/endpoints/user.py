import json

import pinject
import requests
from flask import Blueprint, jsonify, request, current_app as app
from app.controllers.user_controller import UserController
from app.definitions.exceptions.app_exceptions import AppException
from app.definitions.service_result import handle_result
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schema.user_schema import CreateUserSchema
from app.services.keycloak_service import AuthService

user = Blueprint("user", __name__)

obj_graph = pinject.new_object_graph(
    modules=None, classes=[UserController, UserRepository, AuthService]
)

user_controller = obj_graph.provide(UserController)


@user.route("/")
def index():
    users = User.query.all()
    return jsonify(
        {"users": users, "status": "Success", "message": "users retrieved"})


# @user.route("/", methods=["POST"])
def create():
    data = request.json
    email = data["email"]
    name = data["name"]

    result = user_controller.create_user({"email": email, "name": name})

    return handle_result(result)


@user.route("/token_login", methods=["POST"])
def login_user():
    data = request.json
    username = data["username"]
    password = data["password"]

    result = user_controller.user_login(
        {
            "username": username,
            "password": password,
        }
    )

    return handle_result(result)


@user.route("/", methods=["POST"])
def register_user():
    schema = CreateUserSchema()
    errors = schema.validate(request.json)

    if errors:
        raise AppException.ValidationException(context=errors)

    data = request.json
    result = user_controller.register_user(
        {
            "username": data["email"],
            "first_name": data["first_name"],
            "last_name": data["last_name"],
            "email": data["email"],
            "password": data["password"]
        }
    )

    return handle_result(result)

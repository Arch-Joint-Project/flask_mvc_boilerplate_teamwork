import pinject
from flask import Blueprint, jsonify, request
from app.controllers.user_controller import UserController
from app.definitions.service_result import handle_result
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schema.user_schema import (
    UserCreate,
    UserLogin,
    AccessToken,
    User as UserSchema,
    RefreshToken,
)
from app.services.keycloak_service import AuthService
from app.utils.validator import validator

user = Blueprint("user", __name__)

obj_graph = pinject.new_object_graph(
    modules=None, classes=[UserController, UserRepository, AuthService]
)

user_controller = obj_graph.provide(UserController)


@user.route("/")
def index():
    users = User.query.all()
    return jsonify({"users": users, "status": "Success", "message": "users retrieved"})


# @user.route("/", methods=["POST"])
def create():
    data = request.json
    email = data["email"]
    name = data["name"]

    result = user_controller.create_user({"email": email, "name": name})

    return handle_result(result)


@user.route("/", methods=["POST"])
@validator(schema=UserCreate())
def register_user():
    """
    ---
    post:
      description: creates a new user
      requestBody:
        required: true
        content:
            application/json:
                schema: UserCreate
      responses:
        '204':
          description: call successful
          content:
            application/json:
              schema: User
      tags:
          - Authentication
    """

    data = request.json
    result = user_controller.register_user(
        {
            "username": data["email"],
            "first_name": data["first_name"],
            "last_name": data["last_name"],
            "email": data["email"],
            "password": data["password"],
        }
    )

    return handle_result(result, schema=UserSchema())


@user.route("/token_login", methods=["POST"])
@validator(schema=UserLogin())
def login_user():
    """
    ---
    post:
      description: logs in a user
      requestBody:
        required: true
        content:
            application/json:
                schema: UserLogin
      responses:
        '200':
          description: call successful
          content:
            application/json:
              schema: AccessToken
      tags:
          - Authentication
    """

    data = request.json
    username = data["email"]
    password = data["password"]

    result = user_controller.user_login(
        {
            "username": username,
            "password": password,
        }
    )

    return handle_result(result, schema=AccessToken())


@user.route("/refresh_token", methods=["POST"])
@validator(schema=RefreshToken())
def refresh_token():
    """
    ---
    post:
      description: logs in a user
      requestBody:
        required: true
        content:
            application/json:
                schema: RefreshToken
      responses:
        '200':
          description: call successful
          content:
            application/json:
              schema: AccessToken
      tags:
          - Authentication
    """

    data = request.json

    result = user_controller.refresh_token(refresh_token=data["refresh_token"])

    return handle_result(result, schema=AccessToken())

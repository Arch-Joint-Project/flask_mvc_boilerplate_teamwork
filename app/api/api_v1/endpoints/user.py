import pinject
import requests
from flask import Blueprint, jsonify, request, current_app as app
from app.controllers.user_controller import UserController
from app.definitions.service_result import handle_result
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.services.keycloak_service import AuthService


class MyBindingSpec(pinject.BindingSpec):
    def configure(self, bind):
        bind("auth_service", to_class=AuthService)


user = Blueprint("user", __name__)


@user.route("/")
def index():

    users = User.query.all()
    return jsonify({"users": users, "status": "Success", "message": "users retrieved"})


@user.route("/", methods=["POST"])
def create():
    data = request.json
    email = data["email"]
    name = data["name"]

    obj_graph = pinject.new_object_graph(
        modules=None, classes=[UserController, UserRepository, AuthService]
    )

    user_controller = obj_graph.provide(UserController)
    result = user_controller.create_user({"email": email, "name": name})

    return handle_result(result)


@user.route("/token_login", methods=["POST"])
def login_user():
    data = request.json
    print(data)
    username = data["username"]
    password = data["password"]

    obj_graph = pinject.new_object_graph(
        modules=None,
        classes=[UserController, UserRepository, AuthService],
        binding_specs=[MyBindingSpec()],
    )

    user_controller = obj_graph.provide(UserController)
    result = user_controller.user_login(
        {
            "username": username,
            "password": password,
        }
    )

    return handle_result(result)

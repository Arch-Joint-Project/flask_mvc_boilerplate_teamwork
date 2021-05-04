import pinject
from flask import Blueprint, jsonify, request
from app.controllers.user_controller import UserController
from app.definitions.service_result import handle_result
from app.models.user import User
from app.repositories.user_repository import UserRepository

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
        modules=None, classes=[UserController, UserRepository]
    )

    user_controller = obj_graph.provide(UserController)
    result = user_controller.create_user({"email": email, "name": name})

    return handle_result(result)

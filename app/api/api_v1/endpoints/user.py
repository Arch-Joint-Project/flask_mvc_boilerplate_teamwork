from flask import Blueprint, jsonify, request
from app.controllers.user_controller import UserController
from app.definitions.service_result import handle_result
from app.models.user import User

user = Blueprint("user", __name__)


@user.route("/")
def index():

    users = User.query.all()
    return jsonify({"users": users, "status": "Success", "message": "users retrieved"})


@user.route("/", methods=["POST"])
def create():
    data = request.json
    print(data)
    email = data["email"]
    name = data["name"]

    result = UserController().create_user({"email": email, "name": name})

    return handle_result(result)

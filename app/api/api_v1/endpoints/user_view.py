# local imports
from app.definitions.service_result import handle_result
from app.schema import (
    UserCreateSchema, UserReadSchema,
    UserUpdateSchema, UserDeleteSchema
)
from app.controllers import UserController
from app.repositories import UserRepository
from app.utils import validator

# third party imports
import pinject
from flask import Blueprint, request

user = Blueprint("user", __name__)

obj_graph = pinject.new_object_graph(modules=None,
                                     classes=[UserController,
                                              UserRepository])

user_controller = obj_graph.provide(UserController)


# customer_controller = CustomerController(CustomerRepository)


@user.route("/", methods=["POST"])
@validator(schema=UserCreateSchema)
def create():
    data = request.json
    user_data = user_controller.create(data)
    return handle_result(user_data, schema=UserCreateSchema)


@user.route("/", methods=["GET"])
def index():
    if not request.args:
        data = user_controller.index()
        return handle_result(data, schema=UserReadSchema, many=True)
    else:
        query_info = request.args.to_dict()
        data = user_controller.find_all(query_info)
        return handle_result(data, schema=UserReadSchema, many=True)


@user.route("/<int:user_id>", methods=["GET"])
def find_by_id(user_id):
    data = user_controller.find_by_id(user_id)
    return handle_result(data, schema=UserReadSchema)


@user.route("/<int:user_id>", methods=["DELETE"])
def delete(user_id):
    data = user_controller.delete(user_id)
    return handle_result(data, schema=UserDeleteSchema)


@user.route('/', methods=["PUT"])
@validator(UserUpdateSchema)
def update():
    query_info = request.args.to_dict()
    obj_in = request.json
    data = user_controller.update(query_info, obj_in)
    return handle_result(data, schema=UserUpdateSchema)


@user.route('/<int:user_id>', methods=["PUT"])
@validator(UserUpdateSchema)
def update_by_id(user_id):
    data = request.json
    new_data = user_controller.update_by_id(user_id, data)
    return handle_result(new_data, schema=UserUpdateSchema)



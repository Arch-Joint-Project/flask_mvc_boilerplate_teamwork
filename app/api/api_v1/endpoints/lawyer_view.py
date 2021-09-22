# local imports
from app.core.service_result import handle_result
from app.schema import (
    LawyerReadSchema, LawyerSigninSchema,
    LawyerCreateSchema
)

from app.controllers import LawyerController
from app.repositories import LawyerRepository
from app.utils import validator
from app.services import RedisService

# third party imports
import pinject
from flask import Blueprint, request, jsonify
from app.utils.token_auth import token_required

lawyer = Blueprint("lawyer", __name__)

obj_graph = pinject.new_object_graph(modules=None,
                                     classes=[LawyerController,
                                              LawyerRepository, RedisService])

lawyer_controller = obj_graph.provide(LawyerController)


# create new lawyer
@lawyer.route("/", methods=["POST"])
@validator(schema=LawyerCreateSchema)
@token_required(role=["admin"])
def create_lawyer(current_user):
    lawyer_data = lawyer_controller.create(request.json, current_user["id"])
    return handle_result(lawyer_data, schema=LawyerReadSchema)


@lawyer.route("/signin", methods=["POST"])
@validator(schema=LawyerSigninSchema)
def signin_lawyer():
    token = lawyer_controller.sign_in(request.json)
    return jsonify({"token": token})


@lawyer.route("/", methods=["GET"])
@token_required(role=["admin"])
def view_lawyers(current_user):
    lawyer_data = lawyer_controller.index()
    return handle_result(lawyer_data, schema=LawyerReadSchema, many=True)


@lawyer.route("/<int:lawyer_id>", methods=["GET"])
@token_required(role=["admin"])
def view_lawyer(current_user, lawyer_id):
    lawyer_data = lawyer_controller.find_by_id(lawyer_id)
    return handle_result(lawyer_data, schema=LawyerReadSchema)


@lawyer.route("/<int:lawyer_id>", methods=["PUT"])
@token_required(role=["admin"])
def update_lawyer(current_user, lawyer_id):
    lawyer_data = lawyer_controller.update_by_id(lawyer_id, request.json)
    return handle_result(lawyer_data, schema=LawyerReadSchema)


@lawyer.route("/<int:lawyer_id>", methods=["DELETE"])
@token_required(role=["admin"])
def delete_lawyer(current_user, lawyer_id):
    lawyer_data = lawyer_controller.delete(lawyer_id)
    return handle_result(lawyer_data)

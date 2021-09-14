# local imports
from app.core.service_result import handle_result
from app.schema import (
    LawyerReadSchema, LawyerSigninSchema,
    LawyerCreateSchema
)

from app.controllers import LawyerController
from app.repositories import LawyerRepository
from app.services.auth import token_required
from app.utils import validator

# third party imports
import pinject
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from app.models import LawyerModel, AdminModel
from app.services import sign_in

lawyer = Blueprint("lawyer", __name__)

obj_graph = pinject.new_object_graph(modules=None,
                                     classes=[LawyerController,
                                              LawyerRepository])

lawyer_controller = obj_graph.provide(LawyerController)


# create new lawyer
@lawyer.route("/", methods=["POST"])
@validator(schema=LawyerCreateSchema)
@token_required
def create_lawyer(current_user):
    user = AdminModel.query.filter_by(**current_user).first()
    if user:
        data = request.json
        data["admin_id"] = current_user["id"]
        # hash incoming password into database
        data["password"] = generate_password_hash(data["password"],
                                                  method="sha256")
        lawyer_data = lawyer_controller.create(data)
        return handle_result(lawyer_data, schema=LawyerReadSchema)
    else:
        return jsonify({
            "status": "error",
            "error": "operation unauthorized"
        })


@lawyer.route("/signin", methods=["POST"])
@validator(schema=LawyerSigninSchema)
def signin_lawyer():
    auth = request.json
    signin_response = sign_in(auth, LawyerModel)
    return signin_response


@lawyer.route("/", methods=["GET"])
@token_required
def view_lawyers(current_user):
    # get info of logged in users based on the id
    user = AdminModel.query.filter_by(**current_user).first()
    if user:
        lawyer_data = lawyer_controller.index()
        return handle_result(lawyer_data, schema=LawyerReadSchema, many=True)
    else:
        lawyer_data = lawyer_controller.find({"id": current_user["id"]})
        # return info
        return handle_result(lawyer_data, schema=LawyerReadSchema)

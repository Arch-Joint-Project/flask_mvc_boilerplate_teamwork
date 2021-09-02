# local imports
from app.core.service_result import handle_result
from app.schema import (
    LawyerCreateSchema, LawyerReadSchema, LawyerSigninSchema
)
from app.controllers import LawyerController
from app.repositories import LawyerRepository
from app.utils import validator

# third party imports
import pinject
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user
from app.models import AdminModel
from werkzeug.security import generate_password_hash

lawyer = Blueprint("lawyer", __name__)

obj_graph = pinject.new_object_graph(modules=None,
                                     classes=[LawyerController,
                                              LawyerRepository])

lawyer_controller = obj_graph.provide(LawyerController)
admin_id_list = [admin.id for admin in AdminModel.query.all()]


@lawyer.route("/signin", methods=["POST"])
@validator(schema=LawyerSigninSchema)
def sign_in():
    auth = request.json
    user = lawyer_controller.signin(auth)
    return user


@lawyer.route("/", methods=["POST"])
@validator(schema=LawyerCreateSchema)
@jwt_required()
# create new lawyers. accessible by only admins
def create():
    if current_user.id not in admin_id_list:
        return jsonify({'status': 'error', 'error': 'operation unauthorized'})
    data = request.json
    data["admin_id"] = current_user.id
    data["password"] = generate_password_hash(data["password"], method="sha256")
    lawyer_data = lawyer_controller.create(data)
    return handle_result(lawyer_data, schema=LawyerReadSchema)


@lawyer.route("/", methods=["GET"])
@jwt_required()
# view all lawyers. accessible by only admins
def index():
    if current_user.id not in admin_id_list:
        print(f'this is {current_user}')
        return jsonify({'status': 'error', 'error': 'operation unauthorized'})
    print(f'this is {current_user}')
    lawyer_data = lawyer_controller.index()
    return handle_result(lawyer_data, schema=LawyerReadSchema, many=True)


@lawyer.route("/home", methods=["GET"])
@jwt_required()
# view lawyer info/home route
def home():
    lawyer_data = lawyer_controller.find_by_id(current_user.id)
    return handle_result(lawyer_data, schema=LawyerReadSchema)


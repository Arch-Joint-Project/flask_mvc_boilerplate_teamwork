# local imports
from app.core.service_result import handle_result
from app.schema import (
    AdminReadSchema, AdminCreateSchema,
    AdminSigninSchema
)
from app.controllers import (
    AdminController
)
from app.repositories import (
    AdminRepository
)
from app.services import RedisService
from app.utils.token_auth import token_required
from app.utils import validator
from app.models import AdminModel
from app.services import AuthService

# third party imports
from werkzeug.security import generate_password_hash
import pinject
from flask import Blueprint, request, jsonify, make_response

admin = Blueprint("admin", __name__)

obj_graph_admin = pinject.new_object_graph(modules=None,
                                           classes=[AdminController,
                                                    AdminRepository, RedisService])
admin_controller = obj_graph_admin.provide(AdminController)

auth = AuthService()


# create new admin
@admin.route("/", methods=["POST"])
@validator(schema=AdminCreateSchema)
def create_admin():
    admin_data = admin_controller.create(request.json)
    return handle_result(admin_data, schema=AdminReadSchema)


@admin.route("/signin", methods=["POST"])
@validator(schema=AdminSigninSchema)
def signin_admin():
    token = admin_controller.sign_in(request.json)
    return jsonify({"token": token})


@admin.route("/", methods=["GET"])
@token_required(role="admin")
def view_admins(current_user):
    admin_data = admin_controller.index()
    return handle_result(admin_data, schema=AdminReadSchema, many=True)


@admin.route("/<int:admin_id>", methods=["GET"])
@token_required(role="admin")
def view_admin(current_user, admin_id):
    admin_data = admin_controller.find_by_id(admin_id)
    return handle_result(admin_data, schema=AdminReadSchema)


@admin.route("/<int:admin_id>", methods=["PUT"])
@token_required(role="admin")
def update_admin(current_user, admin_id):
    admin_data = admin_controller.update(admin_id, request.json)
    return handle_result(admin_data, schema=AdminReadSchema)


@admin.route("/<int:admin_id>", methods=["DELETE"])
@token_required(role="admin")
def delete_admin(current_user, admin_id):
    admin_data = admin_controller.delete(admin_id)
    return handle_result(admin_data)

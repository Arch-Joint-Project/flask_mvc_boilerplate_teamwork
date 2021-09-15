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
from app.services.auth import token_required, sign_in
from app.utils import validator
from app.models import AdminModel

# third party imports
from werkzeug.security import generate_password_hash
import pinject
from flask import Blueprint, request, jsonify

admin = Blueprint("admin", __name__)

obj_graph_admin = pinject.new_object_graph(modules=None,
                                           classes=[AdminController,
                                                    AdminRepository, RedisService])
admin_controller = obj_graph_admin.provide(AdminController)


# create new admin
@admin.route("/", methods=["POST"])
@validator(schema=AdminCreateSchema)
def create_admin():
    data = request.json
    data["password"] = generate_password_hash(data["password"],
                                              method="sha256")
    admin_data = admin_controller.create(data)
    # admin_redis_controller.set("admin_" + data["username"], json.dumps(data))
    return handle_result(admin_data, schema=AdminReadSchema)


@admin.route("/signin", methods=["POST"])
@validator(schema=AdminSigninSchema)
def signin_admin():
    auth = request.json
    signin_response = sign_in(auth, AdminModel)
    return signin_response


@admin.route("/", methods=["GET"])
@token_required
def view_admins(current_user):
    user = AdminModel.query.filter_by(**current_user).first()
    if user:
        admin_data = admin_controller.index()
        return handle_result(admin_data, schema=AdminReadSchema, many=True)
    else:
        return jsonify({
            "status": "error",
            "error": "operation unauthorized"
        })

# local imports
from app.core.service_result import handle_result
from app.schema import (
    AdminReadSchema, AdminCreateSchema
)
from app.controllers import AdminController
from app.repositories import AdminRepository
from app.utils import validator

# third party imports
import pinject
from flask import Blueprint, request

admin = Blueprint("admin", __name__)

obj_graph = pinject.new_object_graph(modules=None,
                                     classes=[AdminController,
                                              AdminRepository])

admin_controller = obj_graph.provide(AdminController)


@admin.route("/", methods=["POST"])
@validator(schema=AdminCreateSchema)
def create():
    data = request.json
    admin_data = admin_controller.create(data)
    return handle_result(admin_data, schema=AdminReadSchema)


@admin.route("/", methods=["GET"])
def home():
    admin_data = admin_controller.index()
    return handle_result(admin_data, schema=AdminReadSchema, many=True)

# @bill.route("/", methods=["GET"])
# def index():
#     data = bill_controller.index()
#     return handle_result(data, schema=BillReadSchema, many=True)
#
#
# @bill.route("/<int:emp_id>/<company>", methods=["GET"])
# def find_by_id(emp_id, company):
#     data = bill_controller.find_by_id((emp_id, company))
#     return handle_result(data, schema=BillReadSchema)
#
#
# @bill.route("/<int:emp_id>", methods=["GET"])
# def find_all(emp_id):
#     data = bill_controller.find_all({"id": emp_id})
#     return handle_result(data, schema=BillReadSchema, many=True)
#
#
# @bill.route("/<int:emp_id>/<company>", methods=["DELETE"])
# def delete(emp_id, company):
#     data = bill_controller.delete((emp_id, company))
#     return handle_result(data, schema=BillDeleteSchema)
#
#
# @bill.route('/', methods=["PUT"])
# @validator(BillUpdateSchema)
# def update():
#     query_info = request.args.to_dict()
#     obj_in = request.json
#     data = bill_controller.update(query_info, obj_in)
#     return handle_result(data, schema=BillUpdateSchema)
#
#
# @bill.route('/<int:emp_id>/<company>', methods=["PUT"])
# @validator(BillUpdateSchema)
# def update_by_id(emp_id, company):
#     data = request.json
#     new_data = bill_controller.update_by_id((emp_id, company), data)
#     return handle_result(new_data, schema=BillUpdateSchema)

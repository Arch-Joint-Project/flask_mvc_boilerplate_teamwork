# local imports
from app.core.service_result import handle_result
from app.schema import (
    BillCreateSchema, BillReadSchema,
    BillDeleteSchema, BillUpdateSchema
)
from app.controllers import BillController
from app.repositories import BillRepository
from app.utils import validator

# third party imports
import pinject
from flask import Blueprint, request

bill = Blueprint("bill", __name__)

obj_graph = pinject.new_object_graph(modules=None,
                                     classes=[BillController,
                                              BillRepository])

bill_controller = obj_graph.provide(BillController)


@bill.route("/", methods=["POST"])
@validator(schema=BillCreateSchema)
def create():
    data = request.json
    lawyer_data = bill_controller.create(data)
    return handle_result(lawyer_data, schema=BillReadSchema)


@bill.route("/", methods=["GET"])
def index():
    data = bill_controller.index()
    return handle_result(data, schema=BillReadSchema, many=True)


@bill.route("/<int:lawyer_id>/<company>", methods=["GET"])
def find_bill(lawyer_id, company):
    param = {
        "lawyer_id": lawyer_id,
        "company": company
    }
    data = bill_controller.find(param)
    return handle_result(data, schema=BillReadSchema)


@bill.route("/<int:lawyer_id>", methods=["GET"])
def find_lawyer_bill(lawyer_id):
    data = bill_controller.find_all({"lawyer_id": lawyer_id})
    return handle_result(data, schema=BillReadSchema, many=True)


@bill.route("/<int:lawyer_id>/<company>", methods=["DELETE"])
def delete(lawyer_id, company):
    param = {
        "lawyer_id": lawyer_id,
        "company": company
    }
    data = bill_controller.delete(param)
    return handle_result(data, schema=BillReadSchema)


@bill.route('/', methods=["PUT"])
@validator(BillUpdateSchema)
def update():
    query_info = request.args.to_dict()
    obj_in = request.json
    data = bill_controller.update(query_info, obj_in)
    return handle_result(data, schema=BillReadSchema)
#
#
# @bill.route('/<int:emp_id>/<company>', methods=["PUT"])
# @validator(BillUpdateSchema)
# def update_by_id(emp_id, company):
#     data = request.json
#     new_data = bill_controller.update_by_id((emp_id, company), data)
#     return handle_result(new_data, schema=BillUpdateSchema)

# local imports
from app.core.service_result import handle_result
from app.schema import (
    BillReadSchema, BillCreateSchema,
    BillUpdateSchema
)

from app.controllers import BillController
from app.repositories import BillRepository
from app.services import RedisService
from app.utils import validator

# third party imports
import pinject
from flask import Blueprint, request, jsonify
from app.models import LawyerModel, AdminModel
from app.utils.token_auth import token_required

bill = Blueprint("bill", __name__)

obj_graph = pinject.new_object_graph(modules=None,
                                     classes=[BillController,
                                              BillRepository, RedisService])
bill_controller = obj_graph.provide(BillController)


@bill.route("/", methods=["GET"])
@token_required(role="admin")
def view_bills(current_user):
    bill_data = bill_controller.index()
    return handle_result(bill_data, schema=BillReadSchema, many=True)


@bill.route("/<int:id>", methods=["GET"])
@token_required(role="lawyer")
def view_bill(current_user, id):
    bill_data = bill_controller.find_by_id(id)
    return handle_result(bill_data, schema=BillReadSchema)


@bill.route("/company/<company>", methods=["GET"])
@token_required(role="admin")
def view_company_bills(current_user, company):
    bill_data = bill_controller.find_all({"company": company})
    return handle_result(bill_data, schema=BillReadSchema, many=True)


@bill.route("/lawyer/company/<company>", methods=["GET"])
@token_required(role="lawyer")
def view_lawyer_company_bills(current_user, company):
    bill_data = bill_controller.find_all(
            {"lawyer_id": current_user["id"], "company": company})
    return handle_result(bill_data, schema=BillReadSchema, many=True)


# create new bill
@bill.route("/", methods=["POST"])
@validator(schema=BillCreateSchema)
@token_required(role="lawyer")
def create_bill(current_user):
    # get incoming bill
    data = request.json
    # add lawyer id to the data
    data["lawyer_id"] = current_user["id"]
    # get all bills within the system
    query_bill = bill_controller.index()
    bills = handle_result(query_bill, schema=BillReadSchema, many=True)
    for bill in bills.json:
        bill_id = bill.pop("id")
        # compare the bills within the system to the incoming data
        if data == bill:
            # if equal data exist
            # create a duplicate key scenario
            data["id"] = bill_id
            break
    bill_data = bill_controller.create(data)
    return handle_result(bill_data, schema=BillReadSchema)


# update bill created by logged in user
@bill.route("/", methods=["PUT"])
@validator(schema=BillUpdateSchema)
@token_required(role="lawyer")
def update_bill(current_user):
    query_info = request.args.to_dict()
    query_info["lawyer_id"] = current_user["id"]
    obj_in = request.json
    # update bill info
    data = bill_controller.update(query_info, obj_in)
    return handle_result(data, schema=BillReadSchema)


# delete bill created by logged in user for specific company
@bill.route("/<int:bill_id>", methods=["DELETE"])
@token_required(role="lawyer")
def delete_bill(current_user, bill_id):
    delete_bill_info = bill_controller.delete(bill_id, current_user["id"])
    response = handle_result(delete_bill_info)
    if response.status_code == 204:
        return jsonify({
            "status": "operation successful"
        })
    return handle_result(delete_bill_info)


# generate invoice for specific company
# param: company name
@bill.route("/invoice/<company>", methods=["GET"])
@token_required(role="admin")
def generate_company_invoice(current_user, company):
    bill_data = bill_controller.generate_invoice({"company": company})
    return handle_result(bill_data)


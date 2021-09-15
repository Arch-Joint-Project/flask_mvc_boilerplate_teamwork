# local imports
from app.core.service_result import handle_result
from app.schema import (
    BillReadSchema, BillCreateSchema,
    BillUpdateSchema
)

from app.controllers import BillController
from app.repositories import BillRepository
from app.services import RedisService
from app.services.auth import token_required
from app.utils import validator

# third party imports
import pinject
from flask import Blueprint, request, jsonify
from app.models import LawyerModel, AdminModel

bill = Blueprint("bill", __name__)

obj_graph = pinject.new_object_graph(modules=None,
                                     classes=[BillController,
                                              BillRepository, RedisService])
bill_controller = obj_graph.provide(BillController)


@bill.route("/", methods=["GET"])
@token_required
def index(current_user):
    # check if current user is admin
    user = AdminModel.query.filter_by(**current_user).first()
    if user:
        bill_data = bill_controller.index()
        return handle_result(bill_data, schema=BillReadSchema, many=True)
    else:
        return jsonify({
            "status": "error",
            "error": "operation unauthorized"
        })


# view all bills created in the system
@bill.route("/search", methods=["GET"])
@token_required
def view_bill(current_user):
    # check if current user is admin
    user = AdminModel.query.filter_by(**current_user).first()
    if user:
        # query all bills in table
        bill_data = bill_controller.find(query_param)
    # current user is lawyer
    else:
        # query bill table based on id
        bill_data = bill_controller.find_all({"lawyer_id": current_user["id"]})
    return handle_result(bill_data, schema=BillReadSchema, many=True)


@bill.route("/company/<company>", methods=["GET"])
@token_required
def view_company_bills(current_user, company):
    user = AdminModel.query.filter_by(**current_user).first()
    if user:
        # get all bills of specified company if user is admin
        bill_data = bill_controller.find_all({"company": company})
    else:
        # get bills of specified company belonging to current user
        bill_data = bill_controller.find_all(
            {"lawyer_id": current_user["id"], "company": company})
    return handle_result(bill_data, schema=BillReadSchema, many=True)


# create new bill
@bill.route("/", methods=["POST"])
@validator(schema=BillCreateSchema)
@token_required
def create_bill(current_user):
    user = AdminModel.query.filter_by(**current_user).first()
    # admins are not supposed to create bills
    if user:
        return jsonify({
            "status": "error",
            "error": "operation not allowed",
            "msg": "bills can only be created by lawyers"
        })
    else:
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


# delete bill created by logged in user for specific company
@bill.route("/<company>", methods=["DELETE"])
@token_required
def delete_bill(current_user, company):
    user = LawyerModel.query.filter_by(**current_user).first()
    if user:
        delete_bill_info = bill_controller.delete(
            {"lawyer_id": current_user["id"], "company": company})
        response = handle_result(delete_bill_info)
        if response.status_code == 204:
            return jsonify({
                "status": "operation successful"
            })
        return handle_result(delete_bill_info)
    else:
        return jsonify({
            "status": "error",
            "error": "operation unauthorized"
        })


# update bill created by logged in user
@bill.route("/", methods=["PUT"])
@validator(schema=BillUpdateSchema)
@token_required
def update_bill(current_user):
    user = LawyerModel.query.filter_by(**current_user).first()
    if user:
        query_info = request.args.to_dict()
        # set lawyer_id of bill to logged in user id
        query_info["lawyer_id"] = current_user["id"]
        obj_in = request.json
        # update bill info
        data = bill_controller.update(query_info, obj_in)
        return handle_result(data, schema=BillReadSchema)
    else:
        return jsonify({
            "status": "error",
            "error": "operation unauthorized"
        })


# generate invoice for specific company
# param: company name
@bill.route("/invoice/<company>", methods=["GET"])
@token_required
def generate_company_invoice(current_user, company):
    user = AdminModel.query.filter_by(**current_user).first()
    if user:
        bill_data = bill_controller.generate_invoice({"company": company})
        return handle_result(bill_data)
    else:
        return jsonify({
            "status": "error",
            "error": "operation unauthorized"
        })


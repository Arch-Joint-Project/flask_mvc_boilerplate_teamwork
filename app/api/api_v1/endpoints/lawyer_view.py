# local imports
from app.core.service_result import handle_result
from app.schema import (
    LawyerReadSchema, BillReadSchema,
    BillCreateSchema, BillUpdateSchema
)

from app.controllers import LawyerController, BillController
from app.repositories import LawyerRepository, BillRepository
from app.utils import validator

# third party imports
import pinject
from flask import Blueprint, request
from app.models import LawyerModel

lawyer = Blueprint("lawyer", __name__)

obj_graph_1 = pinject.new_object_graph(modules=None,
                                       classes=[LawyerController,
                                                LawyerRepository])

obj_graph_2 = pinject.new_object_graph(modules=None,
                                       classes=[BillController,
                                                BillRepository])

lawyer_controller = obj_graph_1.provide(LawyerController)
bill_controller = obj_graph_2.provide(BillController)


# view login in lawyer info
@lawyer.route("/home", methods=["GET"])
def home():
    # get authentication information
    lawyer_data = lawyer_controller.sign_in(request.authorization)
    # check if user is a lawyer
    if isinstance(lawyer_data, LawyerModel):
        # get info of logged in users based on the id
        lawyer_data = lawyer_controller.find({"id": lawyer_data.id})
        # return info
        return handle_result(lawyer_data, schema=LawyerReadSchema)
    # return error info
    return lawyer_data


# view bills created by logged in user
@lawyer.route("/bill", methods=["GET"])
def view_all_bills():
    lawyer_data = lawyer_controller.sign_in(request.authorization)
    if isinstance(lawyer_data, LawyerModel):
        # query all bills of logged in user based on the id
        bill_data = bill_controller.find_all({"lawyer_id": lawyer_data.id})
        # return bills
        return handle_result(bill_data, schema=BillReadSchema, many=True)
    return lawyer_data


# view bills for specific company created by logged in user
@lawyer.route("/bill/company/<company>", methods=["GET"])
def view_company_bills(company):
    lawyer_data = lawyer_controller.sign_in(request.authorization)
    if isinstance(lawyer_data, LawyerModel):
        # query company bills of the logged in users
        bill_data = bill_controller.find_all({"lawyer_id": lawyer_data.id, "company": company})
        # return bills
        return handle_result(bill_data, schema=BillReadSchema, many=True)
    return lawyer_data


# create new bill
@lawyer.route("/bill", methods=["POST"])
# validate incoming data
@validator(schema=BillCreateSchema)
def create_bill():
    lawyer_data = lawyer_controller.sign_in(request.authorization)
    if isinstance(lawyer_data, LawyerModel):
        data = request.json
        # set lawyer_id of bill using the id of the current logged in user
        data["lawyer_id"] = lawyer_data.id
        # query all bills in database
        query_bill = bill_controller.index()
        bills = handle_result(query_bill, schema=BillReadSchema, many=True)
        for bill in bills.json:
            # remove id from bills data return
            bill_id = bill.pop("id")
            # compare incoming bill data to bills data within the database
            if data == bill:
                # bill is already available, set bill id to id already available
                data["id"] = bill_id
                continue
                # insert data with id available with the database
                # this helps to throw duplicate key error
        bill_data = bill_controller.create(data)
        # return response
        return handle_result(bill_data, schema=BillReadSchema)
    return lawyer_data


# delete bill created by logged in user for specific company
@lawyer.route("/bill/<company>", methods=["DELETE"])
def delete_bill(company):
    lawyer_data = lawyer_controller.sign_in(request.authorization)
    if isinstance(lawyer_data, LawyerModel):
        # delete company bill created by logged in user
        delete_bill_info = bill_controller.delete({"lawyer_id": lawyer_data.id, "company": company})
        return handle_result(delete_bill_info, schema=BillReadSchema,
                             many=True)
    return lawyer_data


# update bill created by logged in user
@lawyer.route("/bill", methods=["PUT"])
@validator(schema=BillUpdateSchema)
def update():
    lawyer_data = lawyer_controller.sign_in(request.authorization)
    if isinstance(lawyer_data, LawyerModel):
        query_info = request.args.to_dict()
        # set lawyer_id of bill to logged in user id
        query_info["lawyer_id"] = lawyer_data.id
        obj_in = request.json
        # update bill info
        data = bill_controller.update(query_info, obj_in)
        return handle_result(data, schema=BillReadSchema)

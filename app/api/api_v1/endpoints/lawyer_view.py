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
    lawyer_data = lawyer_controller.sign_in(request.authorization)
    if isinstance(lawyer_data, LawyerModel):
        lawyer_data = lawyer_controller.find({"id": lawyer_data.id})
        return handle_result(lawyer_data, schema=LawyerReadSchema)
    return lawyer_data


# view bills created by logged in user
@lawyer.route("/bill", methods=["GET"])
def view_all_bills():
    lawyer_data = lawyer_controller.sign_in(request.authorization)
    if isinstance(lawyer_data, LawyerModel):
        bill_data = bill_controller.find_all({"lawyer_id": lawyer_data.id})
        return handle_result(bill_data, schema=BillReadSchema, many=True)
    return lawyer_data


# view bills for specific company created by logged in user
@lawyer.route("/bill/company/<company>", methods=["GET"])
def view_company_bills(company):
    lawyer_data = lawyer_controller.sign_in(request.authorization)
    if isinstance(lawyer_data, LawyerModel):
        bill_data = bill_controller.find_all({"company": company})
        return handle_result(bill_data, schema=BillReadSchema, many=True)
    return lawyer_data


# create new bill
@lawyer.route("/bill", methods=["POST"])
@validator(schema=BillCreateSchema)
def create_bill():
    lawyer_data = lawyer_controller.sign_in(request.authorization)
    if isinstance(lawyer_data, LawyerModel):
        data = request.json
        data["lawyer_id"] = lawyer_data.id
        query_bill = bill_controller.index()
        bills = handle_result(query_bill, schema=BillReadSchema, many=True)
        for bill in bills.json:
            bill_id = bill.pop("id")
            if data == bill:
                data["id"] = bill_id
                continue
        bill_data = bill_controller.create(data)
        return handle_result(bill_data, schema=BillReadSchema)
    return lawyer_data


# delete bill created by logged in user for specific company
@lawyer.route("/bill/<company>", methods=["DELETE"])
def delete_bill(company):
    lawyer_data = lawyer_controller.sign_in(request.authorization)
    if isinstance(lawyer_data, LawyerModel):
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
        query_info["lawyer_id"] = lawyer_data.id
        print(query_info)
        obj_in = request.json
        data = bill_controller.update(query_info, obj_in)
        return handle_result(data, schema=BillReadSchema)

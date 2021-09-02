# local imports
from app.core.service_result import handle_result
from app.schema import (
    BillCreateSchema, BillReadSchema,
    BillDeleteSchema, BillUpdateSchema
)
from app.controllers import BillController
from app.repositories import BillRepository
from app.utils import validator
from app.models import AdminModel

# third party imports
import pinject
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    jwt_required, current_user
)

bill = Blueprint("bill", __name__)

obj_graph = pinject.new_object_graph(modules=None,
                                     classes=[BillController,
                                              BillRepository])

bill_controller = obj_graph.provide(BillController)
admin_id_list = [admin.id for admin in AdminModel.query.all()]


@bill.route("/", methods=["POST"])
@validator(schema=BillCreateSchema)
@jwt_required()
def create():
    print(current_user)
    data = request.json
    data["lawyer_id"] = current_user.id
    lawyer_data = bill_controller.create(data)
    return handle_result(lawyer_data, schema=BillReadSchema)


@bill.route("/", methods=["GET"])
@jwt_required()
def index():
    if current_user.id not in admin_id_list:
        print(f'this is {current_user}')
        return jsonify({'status': 'error', 'error': 'operation unauthorized'})
    data = bill_controller.index()
    return handle_result(data, schema=BillReadSchema, many=True)


@bill.route("/home/<company>", methods=["GET"])
@jwt_required()
def find_bill(company):
    param = {
        "lawyer_id": current_user.id,
        "company": company
    }
    data = bill_controller.find(param)
    return handle_result(data, schema=BillReadSchema)


@bill.route("/home", methods=["GET"])
@jwt_required()
def find_lawyer_bill():
    data = bill_controller.find_all({"lawyer_id": current_user.id})
    return handle_result(data, schema=BillReadSchema, many=True)


@bill.route("/home/<company>", methods=["DELETE"])
@jwt_required()
def delete(company):
    param = {
        "lawyer_id": current_user.id,
        "company": company
    }
    data = bill_controller.delete(param)
    return handle_result(data, schema=BillReadSchema)


@bill.route('/', methods=["PUT"])
@validator(BillUpdateSchema)
@jwt_required()
def update():
    query_info = request.args.to_dict()
    query_info["lawyer_id"] = current_user.id

    print(query_info)

    obj_in = request.json
    data = bill_controller.update(query_info, obj_in)
    return handle_result(data, schema=BillReadSchema)


@bill.route("/invoice/<company>", methods=["GET"])
@jwt_required()
def invoice(company):
    if current_user.id not in admin_id_list:
        print(f'this is {current_user}')
        return jsonify({'status': 'error', 'error': 'operation unauthorized'})
    data = bill_controller.generate_invoice({"company": company})
    return handle_result(data)

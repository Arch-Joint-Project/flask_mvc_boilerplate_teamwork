# builtin imports
import dataclasses
import json

# third party imports
import pinject
from flask import Blueprint, request, make_response, jsonify, Response

# local imports
from app.controllers import BillController
from app.repositories import BillRepository
from app.models import BillableHourSchema
bill = Blueprint("bill", __name__)

obj_graph = pinject.new_object_graph(modules=None,
                                     classes=[BillController,
                                              BillRepository])

bill_controller = obj_graph.provide(BillController)


# customer_controller = CustomerController(CustomerRepository)


@bill.route("/", methods=["POST"])
def create():
    data = request.json
    bill_data = bill_controller.create(data)
    response = json.dumps(dataclasses.asdict(bill_data))
    return Response(response, mimetype="application/json", status=201)


@bill.route("/", methods=["GET"])
def index():
    data = bill_controller.index()
    bill_schema = BillableHourSchema()
    bill_data = bill_schema.dump(data, many=True)
    # response = json.dumps(dataclasses.asdict(data))
    # return Response(response, mimetype="application/json", status=200)
    return make_response(jsonify(bill_data))


@bill.route("/<int:emp_id>/<company>", methods=["GET"])
def find_by_id(emp_id, company):
    data = bill_controller.find_by_id((emp_id, company))
    response = json.dumps(dataclasses.asdict(data))
    return Response(response, mimetype="application/json", status=200)


@bill.route("/<int:emp_id>", methods=["GET"])
def find_all(emp_id):
    data = bill_controller.find_all({"id": emp_id})
    bill_schema = BillableHourSchema()
    bill_data = bill_schema.dump(data, many=True)
    return make_response(jsonify(bill_data))


@bill.route("/<int:emp_id>/<company>", methods=["DELETE"])
def delete(emp_id, company):
    data = bill_controller.delete((emp_id, company))
    return make_response(jsonify({"status": "success", "msg": "resource deleted"}))


@bill.route('/', methods=["PUT"])
def update():
    query_info = request.args.to_dict()
    print(query_info)
    obj_in = request.json
    data = bill_controller.update(query_info, obj_in)
    return make_response(jsonify(data))


@bill.route('/<int:id>/<company>', methods=["PUT"])
def update_by_id(id, company):
    data = request.json
    new_data = bill_controller.update_by_id((id, company), data)
    return make_response(jsonify(new_data))



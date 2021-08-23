# local imports
from app.definitions.service_result import handle_result
from app.schema import (
    BillUpdateSchema, BillCreateSchema,
    BillReadSchema, BillDeleteSchema
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


# customer_controller = CustomerController(CustomerRepository)


@bill.route("/", methods=["POST"])
@validator(schema=BillCreateSchema)
def create():
    data = request.json
    bill_data = bill_controller.create(data)
    return handle_result(bill_data, schema=BillCreateSchema)


@bill.route("/", methods=["GET"])
def index():
    data = bill_controller.index()
    return handle_result(data, schema=BillReadSchema, many=True)


@bill.route("/<int:emp_id>/<company>", methods=["GET"])
def find_by_id(emp_id, company):
    data = bill_controller.find_by_id((emp_id, company))
    return handle_result(data, schema=BillReadSchema)


@bill.route("/<int:emp_id>", methods=["GET"])
def find_all(emp_id):
    data = bill_controller.find_all({"id": emp_id})
    return handle_result(data, schema=BillReadSchema, many=True)


@bill.route("/<int:emp_id>/<company>", methods=["DELETE"])
def delete(emp_id, company):
    data = bill_controller.delete((emp_id, company))
    return handle_result(data, schema=BillDeleteSchema)


@bill.route('/', methods=["PUT"])
@validator(BillUpdateSchema)
def update():
    query_info = request.args.to_dict()
    obj_in = request.json
    data = bill_controller.update(query_info, obj_in)
    return handle_result(data, schema=BillUpdateSchema)


@bill.route('/<int:emp_id>/<company>', methods=["PUT"])
@validator(BillUpdateSchema)
def update_by_id(emp_id, company):
    data = request.json
    new_data = bill_controller.update_by_id((emp_id, company), data)
    return handle_result(new_data, schema=BillUpdateSchema)

@bill.route('/generate-invoice', methods=['GET'])
def generate_invoice():
    company = request.args.getall() # @@TODO: handle request as dictionary to pass to wrapper filter_by()
    print(company)
    the_company_record = bill_controller.generate_invoice(company)
    print(the_company_record)
    return ""

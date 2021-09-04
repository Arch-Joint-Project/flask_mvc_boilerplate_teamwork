# local imports
from app.core.service_result import handle_result
from app.schema import (
    AdminReadSchema, AdminCreateSchema,
    LawyerReadSchema, LawyerCreateSchema,
    BillReadSchema
)
from app.controllers import AdminController, LawyerController, BillController
from app.repositories import AdminRepository, LawyerRepository, BillRepository
from app.utils import validator
from werkzeug.security import generate_password_hash
from app.models import AdminModel

# third party imports
import pinject
from flask import Blueprint, request

admin = Blueprint("admin", __name__)

obj_graph_admin = pinject.new_object_graph(modules=None,
                                           classes=[AdminController,
                                                    AdminRepository])
admin_controller = obj_graph_admin.provide(AdminController)

obj_graph_lawyer = pinject.new_object_graph(modules=None,
                                            classes=[LawyerController,
                                                     LawyerRepository])

lawyer_controller = obj_graph_lawyer.provide(LawyerController)

obj_graph_bill = pinject.new_object_graph(modules=None,
                                          classes=[BillController,
                                                   BillRepository])

bill_controller = obj_graph_bill.provide(BillController)


# create new admin
@admin.route("/", methods=["POST"])
@validator(schema=AdminCreateSchema)
def create_admin():
    data = request.json
    data["password"] = generate_password_hash(data["password"],
                                              method="sha256")
    admin_data = admin_controller.create(data)
    return handle_result(admin_data, schema=AdminReadSchema)


# view all admins in db
@admin.route("/", methods=["GET"])
def view_all_admins():
    admin_data = admin_controller.sign_in(request.authorization)
    if isinstance(admin_data, AdminModel):
        admin_data = admin_controller.index()
        return handle_result(admin_data, schema=AdminReadSchema, many=True)
    return admin_data


# create new lawyer
@admin.route("/lawyer", methods=["POST"])
@validator(schema=LawyerCreateSchema)
def create_lawyer():
    admin_data = admin_controller.sign_in(request.authorization)
    if isinstance(admin_data, AdminModel):
        data = request.json
        data["admin_id"] = admin_data.id
        data["password"] = generate_password_hash(data["password"],
                                                  method="sha256")
        lawyer_data = lawyer_controller.create(data)
        return handle_result(lawyer_data, schema=LawyerReadSchema)
    return admin_data


# view all layers in db
@admin.route("/lawyer", methods=["GET"])
def view_all_lawyers():
    admin_data = admin_controller.sign_in(request.authorization)
    if isinstance(admin_data, AdminModel):
        lawyer_data = lawyer_controller.index()
        return handle_result(lawyer_data, schema=LawyerReadSchema, many=True)
    return admin_data


# view specific lawyer
# param: lawyer username
@admin.route("/lawyer/<username>", methods=["GET"])
def view_lawyer(username):
    admin_data = admin_controller.sign_in(request.authorization)
    if isinstance(admin_data, AdminModel):
        lawyer_data = lawyer_controller.find({"username": username})
        return handle_result(lawyer_data, schema=LawyerReadSchema)
    return admin_data


# view all bills created in the system
@admin.route("/bill", methods=["GET"])
def get_bills():
    admin_data = admin_controller.sign_in(request.authorization)
    if isinstance(admin_data, AdminModel):
        bill_data = bill_controller.index()
        return handle_result(bill_data, schema=BillReadSchema, many=True)
    return admin_data


# view bill created by specific lawyer to specific company
# param: lawyer username, company name
@admin.route("/bill/<lawyer_username>/<company>", methods=["GET"])
def get_bill(lawyer_username, company):
    admin_data = admin_controller.sign_in(request.authorization)
    if isinstance(admin_data, AdminModel):
        lawyer_data = lawyer_controller.find({"username": lawyer_username})
        lawyer = handle_result(lawyer_data, schema=LawyerReadSchema)
        bill_data = bill_controller.find(
            {"lawyer_id": lawyer.json["id"], "company": company})
        return handle_result(bill_data, schema=BillReadSchema)
    return admin_data


# view bills created by specific lawyers
# param: lawyer username
@admin.route("/bill/lawyer/<lawyer_username>", methods=["GET"])
def get_lawyer_bills(lawyer_username):
    admin_data = admin_controller.sign_in(request.authorization)
    if isinstance(admin_data, AdminModel):
        lawyer_data = lawyer_controller.find({"username": lawyer_username})
        lawyer = handle_result(lawyer_data, schema=LawyerReadSchema)
        bill_data = bill_controller.find_all({"lawyer_id": lawyer.json["id"]})
        return handle_result(bill_data, schema=BillReadSchema, many=True)
    return admin_data


# view bills created for specific company
# param: company name
@admin.route("/bill/company/<company>", methods=["GET"])
def get_company_bills(company):
    admin_data = admin_controller.sign_in(request.authorization)
    if isinstance(admin_data, AdminModel):
        bill_data = bill_controller.find_all({"company": company})
        return handle_result(bill_data, schema=BillReadSchema, many=True)
    return admin_data


# generate invoice for specific company
# param: company name
@admin.route("/bill/invoice/<company>", methods=["GET"])
def get_company_invoice(company):
    print('i am invoice')
    admin_data = admin_controller.sign_in(request.authorization)
    if isinstance(admin_data, AdminModel):
        bill_data = bill_controller.generate_invoice({"company": company})
        return handle_result(bill_data)
    return admin_data

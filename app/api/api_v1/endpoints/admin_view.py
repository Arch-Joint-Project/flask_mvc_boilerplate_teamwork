# local imports
import json

from app.controllers.lawyer_redis_service_controller import \
    LawyerRedisController
from app.core.service_result import handle_result
from app.repositories.lawyer_redis_repository import LawyerRedisRepository
from app.schema import (
    AdminReadSchema, AdminCreateSchema,
    LawyerReadSchema, LawyerCreateSchema,
    BillReadSchema, AdminSigninSchema
)
from app.controllers import (
    AdminController, LawyerController,
    BillController, AdminRedisController
)
from app.repositories import (
    AdminRepository, LawyerRepository,
    BillRepository, AdminRedisRepository
)
from app.services import RedisService
from app.services.auth import token_required, sign_in
from app.utils import validator
from app.models import AdminModel

# third party imports
from werkzeug.security import generate_password_hash
import pinject
from flask import Blueprint, request, jsonify

admin = Blueprint("admin", __name__)

obj_graph_admin = pinject.new_object_graph(modules=None,
                                           classes=[AdminController,
                                                    AdminRepository])
admin_controller = obj_graph_admin.provide(AdminController)

obj_graph_lawyer = pinject.new_object_graph(modules=None,
                                            classes=[LawyerController,
                                                     LawyerRepository,
                                                     RedisService])

lawyer_controller = obj_graph_lawyer.provide(LawyerController)

obj_graph_bill = pinject.new_object_graph(modules=None,
                                          classes=[BillController,
                                                   BillRepository])

bill_controller = obj_graph_bill.provide(BillController)

# lawyer redis dependency injection
obj_graph_lawyer_redis = pinject.new_object_graph(modules=None,
                                          classes=[LawyerRedisController,
                                                   LawyerRedisRepository])


# lawyer redis.
lawyer_redis_service_controller = obj_graph_lawyer_redis.provide(LawyerRedisController)



obj_graph_admin_redis = pinject.new_object_graph(modules=None,
                                          classes=[AdminRedisController,
                                                   AdminRedisRepository])

admin_redis_controller = obj_graph_admin_redis.provide(AdminRedisController)


# create new admin
@admin.route("/", methods=["POST"])
# validate incoming data
@validator(schema=AdminCreateSchema)
def create_admin():
    data = request.json
    data["password"] = generate_password_hash(data["password"],
                                              method="sha256")
    admin_data = admin_controller.create(data)
    # cache admin data
    # add 'admin' to the key to serve as a pattern for retrieving all records
    admin_redis_controller.set("admin_" + data["username"], json.dumps(data))
    return handle_result(admin_data, schema=AdminReadSchema)


# signin admin
@admin.route("/signin", methods=["POST"])
# validate incoming data
@validator(schema=AdminSigninSchema)
def signin_admin():
    auth = request.json
    signin_response = sign_in(auth, AdminModel)
    return signin_response


# view all admins in db
@admin.route("/", methods=["GET"])
@token_required(model=AdminModel)
def view_all_admins(current_user):
    # retrieve all admins using the 'admin' as a pattern
    admin_data = admin_redis_controller.get_all("admin_*")
    check_result = handle_result(admin_data)
    # check if data exist in cache
    if len(check_result.json) == 0:
        # if not contact server
        admin_data = admin_controller.index()
    return handle_result(admin_data, schema=AdminReadSchema, many=True)


# create new lawyer
@admin.route("/lawyer", methods=["POST"])
@token_required(model=AdminModel)
@validator(schema=LawyerCreateSchema)
def create_lawyer(current_user):
    data = request.json
    data["admin_id"] = current_user.id
    # hash incoming password into database
    data["password"] = generate_password_hash(data["password"],
                                              method="sha256")
    lawyer_data = lawyer_controller.create(data)
    # cache data
    # add 'lawyer' to the key to serve as a pattern for retrieving all records
    lawyer_redis_service_controller.set("lawyer_" + data["username"], json.dumps(data))
    return handle_result(lawyer_data, schema=LawyerReadSchema)


# view all lawyers in db
@admin.route("/lawyer", methods=["GET"])
@token_required(model=AdminModel)
def view_all_lawyers(current_user):
    # retrieve all lawyers using 'lawyer' as a pattern
    lawyer_data = lawyer_redis_service_controller.get_all("lawyer_*")
    check_result = handle_result(lawyer_data)
    # check if data exist in cache
    if len(check_result.json) == 0:
        # if not contact server
        lawyer_data = lawyer_controller.index()
    return handle_result(lawyer_data, schema=LawyerReadSchema, many=True)


# view specific lawyer
# param: lawyer username
@admin.route("/lawyer/<username>", methods=["GET"])
@token_required(model=AdminModel)
def view_lawyer(current_user, username):
    # query lawyer using username provided
    lawyer_data = lawyer_redis_service_controller.get(username)
    cache_result = handle_result(lawyer_data)
    if cache_result.json is None:
        lawyer_data = lawyer_controller.find({"username": username})
        cache_data = handle_result(lawyer_data, schema=LawyerReadSchema).json
        lawyer_redis_service_controller.set(username, json.dumps(cache_data))
    # return query lawyer to user
    return handle_result(lawyer_data, schema=LawyerReadSchema)


# view all bills created in the system
@admin.route("/bill", methods=["GET"])
@token_required(model=AdminModel)
def get_bills(current_user):
    bill_data = bill_controller.index()
    return handle_result(bill_data, schema=BillReadSchema, many=True)


# view bill created by specific lawyer to specific company
# param: lawyer username, company name
@admin.route("/bill/lawyer/<lawyer_username>/company/<company>", methods=["GET"])
@token_required(model=AdminModel)
def get_bill(current_user, lawyer_username, company):
    lawyer_data = lawyer_controller.find({"username": lawyer_username})
    lawyer = handle_result(lawyer_data, schema=LawyerReadSchema).json
    # query bill based on lawyer_id and company name
    bill_data = bill_controller.find(
        {"lawyer_id": lawyer["id"], "company": company})
    # return result
    return handle_result(bill_data, schema=BillReadSchema)


# view bills created by specific lawyers
# param: lawyer username
@admin.route("/bill/lawyer/<lawyer_username>", methods=["GET"])
@token_required(model=AdminModel)
def get_lawyer_bills(current_user, lawyer_username):
    # query lawyer info from username provided
    query_response = lawyer_controller.find({"username": lawyer_username})
    lawyer = handle_result(query_response, schema=LawyerReadSchema).json
    # query bills based on id of queried lawyer
    bill_data = bill_controller.find_all({"lawyer_id": lawyer["id"]})
    return handle_result(bill_data, schema=BillReadSchema, many=True)


# view bills created for specific company
# param: company name
@admin.route("/bill/company/<company>", methods=["GET"])
@token_required(model=AdminModel)
def get_company_bills(current_user, company):
    # query bill based on company name provided
    bill_data = bill_controller.find_all({"company": company})
    # return result
    return handle_result(bill_data, schema=BillReadSchema, many=True)


# generate invoice for specific company
# param: company name
@admin.route("/bill/invoice/<company>", methods=["GET"])
@token_required(model=AdminModel)
def get_company_invoice(current_user, company):
    bill_data = bill_controller.generate_invoice({"company": company})
    return handle_result(bill_data)

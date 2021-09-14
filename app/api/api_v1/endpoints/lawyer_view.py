# local imports
import json


from app.core.service_result import handle_result
from app.schema import (
    LawyerReadSchema, BillReadSchema,
    BillCreateSchema, BillUpdateSchema,
    LawyerSigninSchema
)

from app.controllers import LawyerController, BillController
from app.repositories import LawyerRepository, BillRepository
from app.services.auth import token_required
from app.utils import validator
from werkzeug.security import check_password_hash
from app.services import decode_token, create_token
# third party imports
import pinject
from flask import Blueprint, request, jsonify, make_response
from app.models import LawyerModel
from app.services import sign_in
from app.services import RedisService # import redis service

lawyer = Blueprint("lawyer", __name__)

obj_graph_1 = pinject.new_object_graph(modules=None,
                                       classes=[LawyerController,
                                                LawyerRepository,RedisService])

obj_graph_2 = pinject.new_object_graph(modules=None,
                                       classes=[BillController,
                                                BillRepository])

lawyer_controller = obj_graph_1.provide(LawyerController)
bill_controller = obj_graph_2.provide(BillController)



'''
# signin lawyer
@lawyer.route("/signin", methods=["POST"])
# validate incoming data
@validator(schema=LawyerSigninSchema)
def signin_lawyer():
    auth = request.json
    signin_response = sign_in(auth, LawyerModel)
    return signin_response

'''
# view login in lawyer info
@lawyer.route("/", methods=["GET"])
@token_required(model=LawyerModel)
def index(current_user):
    # get info of logged in users based on the id
    lawyer_data = lawyer_controller.find({"id": current_user.id})
    # return info
    return handle_result(lawyer_data, schema=LawyerReadSchema)


'''
# view bills created by logged in user
@lawyer.route("/bill", methods=["GET"])
@token_required(model=LawyerModel)
def view_all_bills(current_user):

    # redis search key
    bill_key = "bill_" + current_user.id

    # find from redis database first.
    from_redis_bills = lawyer_redis_service_controller.get_all(bill_key)

    # if exist in redis_databases then we are good to query from redis
    if from_redis_bills is not None:
        return handle_result(from_redis_bills,schema=BillReadSchema,many=True)
    else :
        # query all bills of logged in user based on the id
        bill_data = bill_controller.find_all({"lawyer_id": current_user.id})
        # return bills
        return handle_result(bill_data, schema=BillReadSchema, many=True)


# view bills for specific company created by logged in user
@lawyer.route("/bill/company/<company>", methods=["GET"])
@token_required(model=LawyerModel)
def view_company_bills(current_user, company):
    # query company bills of the logged in users
    bill_data = bill_controller.find_all(
        {"lawyer_id": current_user.id, "company": company})

    # return bills
    return handle_result(bill_data, schema=BillReadSchema, many=True)


# create new bill
@lawyer.route("/bill", methods=["POST"])
@token_required(model=LawyerModel)
@validator(schema=BillCreateSchema)
def create_bill(current_user):
    data = request.json
    lawyer_id =  data["lawyer_id"] = current_user.id
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

    # redis key for bill creation
    bill_key = "bill_" + lawyer_id # key to redis

    # lawyer create bills in redis.
    lawyer_redis_service_controller.set(bill_key,json.dumps(data))

    # return response
    return handle_result(bill_data, schema=BillReadSchema)


# delete bill created by logged in user for specific company
@lawyer.route("/bill/<company>", methods=["DELETE"])
@token_required(model=LawyerModel)
def delete_bill(current_user, company):
    # delete company bill created by logged in user
    delete_bill_info = bill_controller.delete(
        {"lawyer_id": current_user.id, "company": company})

    # key to delete from redis
    bill_key = "bill_"+current_user.id

    # delete from redis
    lawyer_redis_service_controller.delete(bill_key)

    # delete from POSTGRESQL
    return handle_result(delete_bill_info, schema=BillReadSchema,
                         many=True)


# update bill created by logged in user
@lawyer.route("/bill", methods=["PUT"])
@token_required(model=LawyerModel)
@validator(schema=BillUpdateSchema)
def update(current_user):
    query_info = request.args.to_dict()
    # set lawyer_id of bill to logged in user id
    query_info["lawyer_id"] = current_user.id
    obj_in = request.json

    # key to update in redis.
    bill_key = "bill_" + current_user.id
    for_redis_data = json.dumps(obj_in)

    # update in redis.
    lawyer_redis_service_controller.set(bill_key,for_redis_data)

    # update bill info in POSTGRES
    data = bill_controller.update(query_info, obj_in)

    return handle_result(data, schema=BillReadSchema)
'''

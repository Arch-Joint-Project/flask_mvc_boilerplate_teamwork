from app.core.result import Result
from app.core.service_result import ServiceResult
from app.repositories import LawyerRepository
from werkzeug.security import check_password_hash
from flask import jsonify, make_response


class LawyerController:
    def __init__(self, lawyer_repository: LawyerRepository):
        self.lawyer_repository = lawyer_repository

    def index(self):
        lawyer = self.lawyer_repository.index()
        return ServiceResult(Result(lawyer, 200))

    def create(self, data):
        lawyer = self.lawyer_repository.create(data)
        return ServiceResult(Result(lawyer, 201))

    def find(self, query_param):
        lawyer = self.lawyer_repository.find(query_param)
        Laywe
        return ServiceResult(Result(lawyer, 200))

    def find_all(self, query_param):
        lawyer = self.lawyer_repository.find_all(query_param)
        return ServiceResult(Result(lawyer, 200))

    def find_by_id(self, obj_id):
        lawyer = self.lawyer_repository.find_by_id(obj_id)
        return ServiceResult(Result(lawyer, 200))

    def delete(self, obj_id):
        lawyer = self.lawyer_repository.delete(obj_id)
        return ServiceResult(Result(lawyer, 200))

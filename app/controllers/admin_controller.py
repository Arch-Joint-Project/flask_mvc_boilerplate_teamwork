from app.core.result import Result
from app.core.service_result import ServiceResult
from app.repositories import AdminRepository
from flask import make_response, jsonify
from werkzeug.security import check_password_hash


class AdminController:
    def __init__(self, admin_repository: AdminRepository):
        self.admin_repository = admin_repository

    def index(self):
        admin = self.admin_repository.index()
        return ServiceResult(Result(admin, 200))

    def create(self, data):
        admin = self.admin_repository.create(data)
        return ServiceResult(Result(admin, 201))

    def find(self, query_param):
        lawyer = self.admin_repository.find(query_param)
        return ServiceResult(Result(lawyer, 200))

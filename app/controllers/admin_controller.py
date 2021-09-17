from flask import jsonify

from app.core.result import Result
from app.core.service_result import ServiceResult
from app.repositories import AdminRepository
from app.models import AdminModel
from app.services.auth import AuthService

auth = AuthService()


class AdminController:
    def __init__(self, admin_repository: AdminRepository):
        self.admin_repository = admin_repository

    def index(self):
        admin = self.admin_repository.index()
        return ServiceResult(Result(admin, 200))

    def create(self, data):
        admin = self.admin_repository.create(data)
        return ServiceResult(Result(admin, 201))

    def find_by_id(self, obj_id):
        # data is coming from url.
        admin = self.admin_repository.find_by_id(obj_id)
        return ServiceResult(Result(admin, 200))

    def update(self, obj_id, obj_in):
        # data is coming from url.
        admin = self.admin_repository.update_by_id(obj_id, obj_in)
        return ServiceResult(Result(admin, 200))

    def delete(self, obj_id):
        # data is coming from url.
        admin = self.admin_repository.delete(obj_id)
        return ServiceResult(Result(admin, 204))

    def sign_in(self, auth_info):
        if not auth_info or not auth_info["username"] or not auth_info[
            "password"]:
            return jsonify({
                "status": "error",
                "error": "authentication information required"
            })
        admin = AdminModel.query.filter_by(
            username=auth_info["username"]).first()
        if admin is not None and admin.verify_password(
            auth_info["password"]):
            return auth.create_token(admin.id, role="admin")
        return jsonify({
            "status": "error",
            "error": "user verification failure. invalid credentials"
        })

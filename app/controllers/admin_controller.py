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
        admin = self.admin_repository.find_by_id(obj_id)
        return ServiceResult(Result(admin, 200))

    def update_by_id(self, obj_id, obj_in):
        admin = self.admin_repository.update_by_id(obj_id, obj_in)
        return ServiceResult(Result(admin, 200))

    def delete(self, obj_id):
        admin = self.admin_repository.delete(obj_id)
        return ServiceResult(Result(admin, 204))

    def sign_in(self, auth_info):
        return auth.sign_in(auth_info, AdminModel, role="admin")

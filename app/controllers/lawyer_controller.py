from app.core.result import Result
from app.core.service_result import ServiceResult
from app.repositories import LawyerRepository
from app.models import LawyerModel
from app.services import AuthService

auth = AuthService()


class LawyerController:
    def __init__(self, lawyer_repository: LawyerRepository):
        self.lawyer_repository = lawyer_repository

    def index(self):
        lawyer = self.lawyer_repository.index()
        return ServiceResult(Result(lawyer, 200))

    def create(self, data, id):
        data["admin_id"] = id
        lawyer = self.lawyer_repository.create(data)
        return ServiceResult(Result(lawyer, 201))

    def find_by_id(self, obj_id):
        lawyer = self.lawyer_repository.find_by_id(obj_id)
        return ServiceResult(Result(lawyer, 200))

    def update_by_id(self, obj_id, obj_in):
        lawyer = self.lawyer_repository.update_by_id(obj_id, obj_in)
        return ServiceResult(Result(lawyer, 200))

    def delete(self, obj_id):
        lawyer = self.lawyer_repository.delete(obj_id)
        return ServiceResult(Result(lawyer, 204))

    def sign_in(self, auth_info):
        return auth.sign_in(auth_info, LawyerModel, role="lawyer")

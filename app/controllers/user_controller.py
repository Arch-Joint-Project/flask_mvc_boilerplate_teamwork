from app.definitions.result import Result
from app.definitions.service_result import ServiceResult
from app.repositories import UserRepository


class UserController:
    def __init__(self, user_repository: UserRepository):
        self.repository = user_repository

    def index(self):
        user = self.repository.index()
        return ServiceResult(Result(user, 200))

    def create(self, data):
        user = self.repository.create(data)
        return ServiceResult(Result(user, 201))

    def find_by_id(self, user_id):
        user = self.repository.find_by_id(user_id)
        return ServiceResult(Result(user, 200))

    def find_all(self, user_id):
        user = self.repository.find_all(user_id)
        return ServiceResult(Result(user, 200))

    def delete(self, user_id):
        user = self.repository.delete(user_id)
        return ServiceResult(Result(user, 204))

    def update(self, query_info, obj_in):
        user = self.repository.update(query_info, obj_in)
        return ServiceResult(Result(user, 200))

    def update_by_id(self, obj_id, obj_in):
        user = self.repository.update_by_id(obj_id, obj_in)
        return ServiceResult(Result(user, 200))

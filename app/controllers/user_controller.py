from app.definitions.repository_interfaces.user_repository_interface import (
    UserRepositoryInterface,
)
from app.definitions.result import Result
from app.definitions.service_result import ServiceResult


class UserController:
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def create_user(self, user_data):
        user = self.user_repository.create(obj_in=user_data)
        return ServiceResult(Result(user, status_code=200))

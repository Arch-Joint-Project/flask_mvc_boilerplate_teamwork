import os
import requests
from flask import current_app as app
from app.definitions.repository_interfaces.user_repository_interface import (
    UserRepositoryInterface,
)
from app.definitions.result import Result
from app.definitions.service_interfaces.auth_service_interface import (
    AuthServiceInterface,
)
from app.definitions.service_result import ServiceResult


class UserController:
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        auth_service: AuthServiceInterface,
    ):
        self.user_repository = user_repository
        self.auth_service = auth_service

    def create_user(self, user_data):
        user = self.user_repository.create(obj_in=user_data)
        return ServiceResult(Result(user, status_code=200))

    def user_login(self, user_data):
        token = self.auth_service.get_token(user_data)
        return ServiceResult(Result(token, status_code=200))

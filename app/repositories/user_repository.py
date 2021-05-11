from app.definitions.repository_interfaces.user_repository_interface import (
    UserRepositoryInterfaceInterface,
)
from app.models.user import User
from .base import SQLBaseRepositoryInterface


class UserRepository(SQLBaseRepositoryInterface,
                     UserRepositoryInterfaceInterface):
    def __init__(self):
        super(UserRepository, self).__init__(model=User)

from app.definitions.repository.user_repository_interface import (
    UserRepositoryInterfaceInterface,
)
from app.models.user import User
from app.definitions.repository.base import SQLBaseRepository


class UserRepository(SQLBaseRepository,
                     UserRepositoryInterfaceInterface):
    model = User

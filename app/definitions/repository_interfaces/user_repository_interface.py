from abc import ABC

from .base.crud_repository_interface import CRUDRepositoryInterface


class UserRepositoryInterfaceInterface(CRUDRepositoryInterface, ABC):
    pass

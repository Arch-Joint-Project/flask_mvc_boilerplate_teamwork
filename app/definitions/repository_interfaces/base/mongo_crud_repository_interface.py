from abc import ABC

from app.definitions.repository_interfaces.base.crud_repository_interface import (
    CRUDRepositoryInterface,
)


class MongoCRUDRepositoryInterfaceInterface(CRUDRepositoryInterface, ABC):
    pass

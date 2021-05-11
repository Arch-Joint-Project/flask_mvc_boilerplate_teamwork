from app.definitions.repository_interfaces.client_repository_interface import \
    ProductRepositoryInterfaceInterface
from app.repositories.base import MongoBaseRepositoryInterface


class ProductRepository(
    ProductRepositoryInterfaceInterface,
    MongoBaseRepositoryInterface
):
    def find_by_id(self, obj_id):
        db_obj = super().find_by_id(id)
        return db_obj

from app.definitions.repository.product_repository_interface import \
    ProductRepositoryInterfaceInterface
from app.models.user import Product
from app.definitions.repository.base import MongoBaseRepository
from app.services.redis_service import RedisService


class ProductRepository(
    ProductRepositoryInterfaceInterface,
    MongoBaseRepository
):
    model = Product

    def __init__(self, redis_service: RedisService):
        self.redis_service = redis_service

    def find_by_id(self, obj_id):
        obj_text = f"product_{obj_id}"
        db_obj = self.redis_service.get(obj_text)
        if db_obj is None:
            db_obj = super().find_by_id(obj_id)
            self.redis_service.set(obj_text, db_obj)
        return db_obj

# local imports
import dataclasses
import json

from app.core.repository import SQLBaseRepository
from app.models import AdminModel
from app.services import RedisService
from app.schema import AdminReadSchema

admin_schema = AdminReadSchema()


class AdminRepository(SQLBaseRepository):
    model=AdminModel

    def __init__(self, redis_service: RedisService):  # make use of redis service
        self.redis_service = redis_service
        super().__init__()

    def create(self, obj_in):
        server_create = super().create(obj_in)
        cache_admin = admin_schema.dumps(server_create)
        cache_all_admin = admin_schema.dumps(super().index(), many=True)
        self.redis_service.set(f"admin__{server_create.id}", cache_admin)  # insert into redis
        self.redis_service.set(f"all_admin", cache_all_admin)
        return server_create

    def index(self):
        all_admin = self.redis_service.get("all_admin")
        if all_admin:
            return all_admin
        return super().index()

    def find_by_id(self, obj_id: int):
        cache_data = self.redis_service.get(f"admin__{obj_id}")
        if cache_data:
            return cache_data
        return super().find_by_id(obj_id)

    def update_by_id(self, obj_id, obj_in):
        cache_data = self.redis_service.get(f"admin__{obj_id}")
        if cache_data:
            self.redis_service.delete(f"admin__{obj_id}")
        server_result = super().update_by_id(obj_id, obj_in)
        self.redis_service.set(f"admin__{obj_id}", admin_schema.dumps(server_result))
        self.redis_service.set("all_admin", admin_schema.dumps(super().index(), many=True))
        return server_result

    def delete(self, obj_id):
        cache_data = self.redis_service.get(f"admin__{obj_id}")
        if cache_data:
            self.redis_service.delete(f"admin__{obj_id}")
        delete = super().delete(obj_id)
        self.redis_service.set("all_admin",
                               admin_schema.dumps(super().index(), many=True))
        return delete


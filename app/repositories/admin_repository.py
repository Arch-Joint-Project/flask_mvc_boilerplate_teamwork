# local imports
import json

from app.core.repository import SQLBaseRepository
from app.models import AdminModel
from app.services import RedisService


class AdminRepository(SQLBaseRepository):
    model=AdminModel


    def __init__(self, redis_service: RedisService): # make use of redis service
        self.redis_service = redis_service
        super().__init__()

    def create(self, obj_in):
        result = super(AdminRepository, self).create(obj_in) # pass data to CRUD
        data = json.dumps(result) # return pass data to json string
        self.redis_service.set(f"admin__{result.id}", data) # insert into redis
        return result

    def find_by_id(self, obj_id: int):
        cached_data = self.redis_service.get(f"admin__{obj_id}")
        if not cached_data:
            return super(AdminRepository, self).find_by_id(obj_id)

        return self.model(**cached_data)



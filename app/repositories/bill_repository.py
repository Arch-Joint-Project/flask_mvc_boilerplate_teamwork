# local imports
import json

from flask import jsonify

from app.core.repository import SQLBaseRepository
from app.models import BillModel
from app.schema import BillReadSchema
from app.services import RedisService
from app.utils import create_time_object, create_date_object

bill_schema = BillReadSchema()


class BillRepository(SQLBaseRepository):
    model = BillModel

    def __init__(self, redis_service: RedisService):
        self.redis_service = redis_service
        super(BillRepository,self).__init__()

    def create(self, obj_in):
        result = super(BillRepository, self).create(obj_in)
        bill_info = bill_schema.dumps(result)
        self.redis_service.set(f"bill__{result.id}", bill_info)
        return result

    def find_by_id(self, obj_id: int):
        cache_data = self.redis_service.get(f"bill__{obj_id}")
        if not cache_data:
            result = super(BillRepository, self).find_by_id(obj_id)
            bill_info = bill_schema.dumps(result)
            self.redis_service.set(f"bill__{obj_id}", bill_info)
            return result
        cache_data["date"] = create_date_object(cache_data["date"])
        cache_data["start_time"] = create_time_object(cache_data["start_time"])
        cache_data["end_time"] = create_time_object(cache_data["end_time"])
        return self.model(**cache_data)

    def update(self, query_info, obj_in):
        model_search = self.find(query_info)
        if model_search:
            self.redis_service.delete(model_search.id)

        result = super(BillRepository, self).update(query_info, obj_in)
        bill_info = bill_schema.dumps(result)
        self.redis_service.set(f"bill__{result.id}", bill_info)
        return result

    def delete(self, query_params):
        bill_info = super(BillRepository, self).find(query_params)
        self.redis_service.delete(f"bill__{bill_info.id}")
        return super(BillRepository, self).delete(bill_info.id)

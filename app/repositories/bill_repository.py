# local imports
import json

from app.core.repository import SQLBaseRepository
from app.models import BillModel
from app.schema import BillReadSchema
from app.services import RedisService

bill_schema = BillReadSchema()


class BillRepository(SQLBaseRepository):
    model = BillModel

    def __init__(self, redis_service: RedisService):
        self.redis_service = redis_service
        super(BillRepository,self).__init__()

    def create(self, obj_in):
        result = super(BillRepository, self).create(obj_in)
        bill_info = bill_schema.dumps(result)
        data = json.dumps(bill_info)
        self.redis_service.set(f"bill__{result.id}", data)
        return result

    def update(self, query_info, obj_in):
        result = super(BillRepository, self).update(query_info, obj_in)
        self.redis_service.delete(result.id)
        bill_info = bill_schema.dumps(result)
        self.redis_service.set(f"bill__{result.id}", bill_info)
        return result

    def delete(self, query_params):
        bill_info = super(BillRepository, self).find(query_params)
        result = super(BillRepository, self).delete(bill_info.id)
        self.redis_service.delete(f"bill__{bill_info.id}")
        return result


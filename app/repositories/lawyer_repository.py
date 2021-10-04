# local imports
from app.core.repository import SQLBaseRepository
from app.models import LawyerModel
from app.services import RedisService
from app.schema import LawyerReadSchema

lawyer_schema = LawyerReadSchema()


class LawyerRepository(SQLBaseRepository):
    model = LawyerModel

    def __init__(self, redis_service: RedisService):
        self.redis_service = redis_service
        super().__init__()

    def create(self, obj_in):
        server_data = super().create(obj_in)
        cache_data = lawyer_schema.dumps(server_data)
        print(cache_data)
        self.redis_service.set(self=self,name=f"lawyer__{server_data.id}",
                                data=cache_data)
        cache_all_lawyers = lawyer_schema.dumps(super().index(), many=True)
        self.redis_service.set(self=self,name="all_lawyers", data=cache_all_lawyers)
        return server_data

    def index(self):
        all_lawyers = self.redis_service.get(self=self,name="all_lawyers")
        if all_lawyers:
            return all_lawyers
        return super().index()

    def find_by_id(self, obj_id: int):
        cache_data = self.redis_service.get(self=self,name=f"lawyer__{obj_id}")
        if cache_data:
            print("cache")
            return cache_data
        return super().find_by_id(obj_id)

    def update_by_id(self, obj_id, obj_in):
        cache_data = self.redis_service.get(f"lawyer__{obj_id}")
        if cache_data:
            self.redis_service.delete(f"lawyer__{obj_id}")
        server_data = super().update_by_id(obj_id, obj_in)
        self.redis_service.set(f"lawyer__{obj_id}",
                               lawyer_schema.dumps(server_data))
        self.redis_service.set("all_lawyers",
                               lawyer_schema.dumps(super().index(), many=True))
        return server_data

    def delete(self, obj_id):
        cache_data = self.redis_service.get(self=self,name=f"lawyer__{obj_id}")
        if cache_data:
            self.redis_service.delete(name=f"lawyer__{obj_id}")
        delete = super().delete(obj_id)
        self.redis_service.set(self=self,name="all_lawyers",
                               data=lawyer_schema.dumps(super().index(), many=True))
        return delete

import mongoengine

from app.definitions.exceptions.app_exceptions import AppException
from app.definitions.repository.base.crud_repository_interface import (
    CRUDRepositoryInterface,
)


class MongoBaseRepository(CRUDRepositoryInterface):
    model: mongoengine

    def index(self):
        return self.model.objects()

    def create(self, obj_in):
        db_obj = self.model(**obj_in)
        db_obj.save()
        return db_obj

    def update_by_id(self, item_id, obj_in):
        db_obj = self.find_by_id(item_id)
        db_obj.modify(**obj_in)
        return db_obj

    def find_by_id(self, obj_id):
        try:
            db_obj = self.model.objects.get(pk=obj_id)
            return db_obj
        except mongoengine.DoesNotExist:
            raise AppException.ResourceDoesNotExist(
                {"error": f"Resource of id {obj_id} does not exist"}
            )

    def delete(self, item_id):
        db_obj = self.find_by_id(item_id)
        db_obj.delete()

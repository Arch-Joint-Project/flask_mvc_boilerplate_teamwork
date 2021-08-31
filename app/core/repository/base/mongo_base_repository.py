import mongoengine
from pymongo.errors import ServerSelectionTimeoutError
from app.core.exceptions.app_exceptions import AppException
from app.core.repository.base.crud_repository_interface import (
    CRUDRepositoryInterface,
)


class MongoBaseRepository(CRUDRepositoryInterface):
    model: mongoengine

    def index(self):
        try:
            return self.model.objects()
        except mongoengine.OperationError:
            raise AppException.OperationError(context="Could not get resource")

    def create(self, obj_in):
        try:
            db_obj = self.model(**obj_in)
            db_obj.save()
            return db_obj
        except mongoengine.OperationError:
            raise AppException.OperationError(context="Could not create resource")
        except ServerSelectionTimeoutError as e:
            raise AppException.InternalServerError(context=e.details)

    def update_by_id(self, obj_id, obj_in):
        try:
            db_obj = self.find_by_id(obj_id)
            db_obj.modify(**obj_in)
            return db_obj
        except mongoengine.OperationError:
            raise AppException.OperationError(context="Could not update resource")
        except ServerSelectionTimeoutError as e:
            raise AppException.InternalServerError(context=e.details)

    def find_by_id(self, obj_id):
        try:
            db_obj = self.model.objects.get(pk=obj_id)
            return db_obj
        except mongoengine.DoesNotExist:
            raise AppException.NotFoundException(
                {"error": f"Resource of id {obj_id} does not exist"}
            )
        except mongoengine.OperationError:
            raise AppException.OperationError("Resource query failed")
        except ServerSelectionTimeoutError as e:
            raise AppException.InternalServerError(context=e.details)

    def find(self, filter_param):
        """
        returns an item that satisfies the data passed to it if it exists in
        the database

        :param filter_param: {dict}
        :return: model_object - Returns an instance object of the model passed
        """
        try:
            db_obj = self.model.objects.get(**filter_param)
            return db_obj
        except mongoengine.DoesNotExist:
            raise AppException.NotFoundException("Resource does not exist")

    def find_all(self, filter_param):
        """
        returns all items that satisfies the filter params passed to it

        :param filter_param: {dict}
        :return: model_object - Returns an instance object of the model passed
        """
        db_obj = self.model.objects(**filter_param)
        return db_obj

    def delete(self, obj_id):
        try:
            db_obj = self.model.objects.get(pk=obj_id)
            db_obj.delete()
            return True
        except mongoengine.DoesNotExist:
            raise AppException.NotFoundException(
                {"error": f"Resource of id {obj_id} does not exist"}
            )
        except mongoengine.OperationError:
            raise AppException.OperationError("Resource deletion failed")
        except ServerSelectionTimeoutError as e:
            raise AppException.InternalServerError(context=e.details)

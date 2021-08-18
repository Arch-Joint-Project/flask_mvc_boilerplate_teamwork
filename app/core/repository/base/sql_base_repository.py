from sqlalchemy.exc import IntegrityError, DBAPIError
from app import db

from app.core.exceptions.app_exceptions import AppException
from app.core.repository.base.crud_repository_interface import (
    CRUDRepositoryInterface,
)


class SQLBaseRepository(CRUDRepositoryInterface):
    model: db.Model

    def __init__(self):
        """
        Base class to be inherited by all repositories. This class comes with
        base crud functionalities attached
        """

        self.db = db

    def index(self):
        """

        :return: {list} returns a list of objects of type model
        """
        try:
            data = self.model.query.all()
        except DBAPIError as e:
            raise AppException.OperationError(context=e.orig.args[0])
        return data

    def create(self, obj_in):
        """

        :param obj_in: the data you want to use to create the model
        :return: {object} - Returns an instance object of the model passed
        """
        try:
            obj_data = dict(obj_in)
            db_obj = self.model(**obj_data)
            self.db.session.add(db_obj)
            self.db.session.commit()
            return db_obj
        except IntegrityError as e:
            raise AppException.OperationError(context=e.orig.args[0])

    def update_by_id(self, obj_id, obj_in):
        """
        :param obj_id: {int}
        :param obj_in: {dict}
        :return: model_object - Returns an instance object of the model passed
        """
        db_obj = self.find_by_id(obj_id)
        if not db_obj:
            raise AppException.NotFoundException(
                f"Resource of id {obj_id} does not exist"
            )
        try:
            for field in obj_in:
                if hasattr(db_obj, field):
                    setattr(db_obj, field, obj_in[field])
            self.db.session.add(db_obj)
            self.db.session.commit()
            return db_obj
        except DBAPIError as e:
            raise AppException.OperationError(context=e.orig.args[0])

    def update(self, query_info, obj_in):
        """
        :param query_info: {dict}
        :param obj_in: {dict}
        :return: model_object - Returns an instance object of the model passed
        """
        db_obj = self.find(query_info)
        if not db_obj:
            raise AppException.NotFoundException("Resource does not exist")
        try:
            for field in obj_in:
                if hasattr(db_obj, field):
                    setattr(db_obj, field, obj_in[field])
            self.db.session.add(db_obj)
            self.db.session.commit()
            return db_obj
        except DBAPIError as e:
            raise AppException.OperationError(context=e.orig.args[0])

    def find_by_id(self, obj_id: int):
        """
        returns a resource matching the specified id if it exists in the database
        :param obj_id: int - id of the resource
        :return: model_object - Returns an instance object of the model passed
        """
        db_obj = self.model.query.get(obj_id)
        if db_obj is None:
            raise AppException.NotFoundException()
        return db_obj

    def find(self, query_params: dict):
        """
        returns a resource matching the query params if it exists in the database
        :param query_params: dict - query parameters
        :return: model_object - Returns an instance object of the model passed
        """
        db_obj = self.model.query.filter_by(**query_params).first()
        if db_obj is None:
            raise AppException.NotFoundException()
        return db_obj

    def find_all(self, data):
        try:
            db_obj = self.model.query.filter_by(**data).all()
        except DBAPIError as e:
            raise AppException.OperationError(context=e.orig.args[0])
        return db_obj

    def delete(self, obj_id):

        """
        deletes a resource if it exists in the database
        :param obj_id:
        :return: returns None
        """

        db_obj = self.find_by_id(obj_id)
        if not db_obj:
            raise AppException.NotFoundException()
        try:
            db.session.delete(db_obj)
            db.session.commit()
        except DBAPIError as e:
            raise AppException.OperationError(context=e.orig.args[0])

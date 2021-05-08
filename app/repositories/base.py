from app import db
from app.definitions.exceptions.HTTPException import HTTPException
from app.definitions.repository_interfaces.base.crud_repository_interface import (
    CRUDRepository,
)


class BaseRepository(CRUDRepository):
    def __init__(self, model):
        """
        Base class to be inherited by all repositories. This class comes with
        base crud functionalities attached

        :param db: Session - sqlalchemy db session to be used for queries
        :param model: base model of the class to be used for queries and returns
        """

        self.db = db
        self.model = model

    def index(self):
        """

        :return: {list} returns a list of objects of type model
        """
        data = self.model.query.all()
        return data

    def create(self, obj_in):
        """

        :param obj_in: the data you want to use to create the model
        :return: {object} - Returns an instance object of the model passed
        """
        obj_data = dict(obj_in)
        db_obj = self.model(**obj_data)
        self.db.session.add(db_obj)
        self.db.session.commit()
        return db_obj

    def update_by_id(self, id, obj_in):
        """

        :param obj_in:
        :return: model_object - Returns an instance object of the model passed
        """
        db_obj = self.find_by_id(id)
        if not db_obj:
            raise HTTPException(status_code=400, description="Resource does not exist")

    def find_by_id(self, id: int):
        """
        returns a user if it exists in the database
        :param id: int - id of the user
        :return: model_object - Returns an instance object of the model passed
        """
        db_obj = self.db.query(self.model).get(id)
        return db_obj

    def delete(self, id):

        """

        :param id:
        :return:
        """

        db_obj = self.find_by_id(id)
        if not db_obj:
            raise HTTPException(status_code=400, description="Resource does not exist")
        db.session.delete(db_obj)
        db.session.commit()

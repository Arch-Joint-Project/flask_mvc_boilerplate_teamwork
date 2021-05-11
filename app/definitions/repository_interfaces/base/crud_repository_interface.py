import abc


class CRUDRepositoryInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            (hasattr(subclass, "index"))
            and callable(subclass.index)
            and hasattr(subclass, "create")
            and callable(subclass.create)
            and hasattr(subclass, "update_by_id")
            and callable(subclass.update_by_id)
            and hasattr(subclass, "find_by_id")
            and callable(subclass.find_by_id)
            and hasattr(subclass, "delete")
            and callable(subclass.delete)
        )

    @abc.abstractmethod
    def index(self):
        """
        when inherited, index should show all data belonging to a model
        :return: obj_data
        """
        raise NotImplementedError

    @abc.abstractmethod
    def create(self, obj_in):
        """
        when inherited, creates a new record
        :param obj_in: the data you want to use to create the model
        :return: obj_data
        """
        raise NotImplementedError

    @abc.abstractmethod
    def update_by_id(self, id, obj_in):
        """
        when inherited, updates a record by taking in the id, and the data you
        want to update with
        :param id:
        :param obj_in:
        :return: a model object
        """

        raise NotImplementedError

    @abc.abstractmethod
    def find_by_id(self, id):
        """
        when inherited, finds a record by id
        :param id:
        :return: a model object
        """

        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, id):
        """
        takes in an id, finds and deletes the record
        :param id:
        :return: model object
        """

        raise NotImplementedError

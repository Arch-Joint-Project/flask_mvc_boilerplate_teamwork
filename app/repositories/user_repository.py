# local imports
from app.definitions.repository import SQLBaseRepository
from app.models import BillableHourModel, UserModel


class UserRepository(SQLBaseRepository):
    model=UserModel

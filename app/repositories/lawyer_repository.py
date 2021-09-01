# local imports
from app.core.repository import SQLBaseRepository
from app.models import LawyerModel


class LawyerRepository(SQLBaseRepository):
    model=LawyerModel
